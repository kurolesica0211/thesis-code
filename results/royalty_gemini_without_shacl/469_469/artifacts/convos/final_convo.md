================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Countess Walburga Douglas (née von Habsburg-Lothringen; born 5 October 1958) is a German-born Swedish lawyer and politician, who served as a member of the Riksdag of Sweden for the Moderate Party from 2006 to 2014.
Early life

Born in 1958 in Berg am Starnberger See, West Germany, she is the fifth daughter of Otto von Habsburg, the last crown prince of Austria-Hungary, and his wife Princess Regina of Saxe-Meiningen.
Walburga was banished from the Republic of Austria from birth and well into adult life, along with her siblings, by the Habsburg Law that had been in effect since 1938, having been (re)imposed by the Nazis.
She is a granddaughter of the last Austrian emperor, Charles I, and a member of the House of Habsburg-Lorraine.
Her ancestral titles (abolished in Austria since 1919) are Archduchess Walburga of Austria, Archduchess of Austria, Princess of Hungary and Bohemia, with the style of Her Imperial and Royal Highness (HI&RH).
She does not currently use her ancestral titles actively in her daily life; however, by law she holds the title of Countess Douglas in the Kingdom of Sweden, her current country of residence and citizenship.
On 17 September 2023, Douglas visited Armenia to dedicate the opening of the PanEuropa Armenia branch in Yerevan.
Personal life

On 5 December 1992 in Budapest, Hungary, Walburga married a Swedish nobleman, Count Carl Axel Archibald Douglas (born 27 November 1949 in Stockholm), son of Count Archibald Douglas and Baroness Margareta Lagerfelt.
Her husband's family is a  noble family in Sweden, descended from the Scot Robert Douglas, Count of Skenninge, member of the Scottish Clan Douglas and founder of its Swedish branch.
Her husband is a first cousin of Count Gustaf Douglas and his sisters Rosita Spencer-Churchill, Duchess of Marlborough, and Princess Elisabeth, Duchess in Bavaria, the wife of Prince Max, Duke in Bavaria.
They have a son, Count Mauritz Otto Wenzel Douglas (born 30 March 1994 in Stockholm).



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (ba1df846-473f-4cfc-9b8d-f0f32d74b7ec)
 Call ID: ba1df846-473f-4cfc-9b8d-f0f32d74b7ec
  Args:
    source: Walburga_Douglas
    type: :Woman
  AssignClass (bef40d9f-642b-44f6-ba89-cca4db4ce85d)
 Call ID: bef40d9f-642b-44f6-ba89-cca4db4ce85d
  Args:
    source: Walburga_Douglas
    type: :Person
  AddLiteral (a7d0825a-33d9-4b12-bc67-2f1f480f91a0)
 Call ID: a7d0825a-33d9-4b12-bc67-2f1f480f91a0
  Args:
    relation: :hasBirthYear
    literal_value: 1958
    source: Walburga_Douglas
    literal_type: xsd:integer
  AssignClass (1921fba4-34ad-409a-9be8-a4f6d7f2ff42)
 Call ID: 1921fba4-34ad-409a-9be8-a4f6d7f2ff42
  Args:
    source: Otto_von_Habsburg
    type: :Man
  AssignClass (e2622685-1576-4b48-94fd-953357282e7b)
 Call ID: e2622685-1576-4b48-94fd-953357282e7b
  Args:
    source: Otto_von_Habsburg
    type: :Person
  AssignClass (fdfb2ae3-40cb-4a93-90fb-31b2af8c3013)
 Call ID: fdfb2ae3-40cb-4a93-90fb-31b2af8c3013
  Args:
    source: Otto_von_Habsburg
    type: :Ancestor
  AssignClass (ac6f853b-8310-4649-afa1-ee66320c5533)
 Call ID: ac6f853b-8310-4649-afa1-ee66320c5533
  Args:
    source: Regina_of_Saxe-Meiningen
    type: :Woman
  AssignClass (7a3e7894-32cd-4bb0-8127-f4448edc636d)
 Call ID: 7a3e7894-32cd-4bb0-8127-f4448edc636d
  Args:
    source: Regina_of_Saxe-Meiningen
    type: :Person
  AssignClass (bcf78fb2-45fd-4ff4-ade5-21c1f3e1ad28)
 Call ID: bcf78fb2-45fd-4ff4-ade5-21c1f3e1ad28
  Args:
    source: Regina_of_Saxe-Meiningen
    type: :Ancestor
  AddTriple (e706d162-e413-4beb-8db6-1768cb3bf124)
 Call ID: e706d162-e413-4beb-8db6-1768cb3bf124
  Args:
    target: Otto_von_Habsburg
    relation: :hasFather
    source: Walburga_Douglas
  AddTriple (53200be6-c7d3-472d-9b9f-72ada454a33e)
 Call ID: 53200be6-c7d3-472d-9b9f-72ada454a33e
  Args:
    target: Regina_of_Saxe-Meiningen
    relation: :hasMother
    source: Walburga_Douglas
  AssignClass (1e14740e-b060-4f03-b1d4-5c7a9ae92b20)
 Call ID: 1e14740e-b060-4f03-b1d4-5c7a9ae92b20
  Args:
    source: Charles_I
    type: :Man
  AssignClass (1ba99900-5d9c-4c5e-8b7a-d2565bbed2f9)
 Call ID: 1ba99900-5d9c-4c5e-8b7a-d2565bbed2f9
  Args:
    source: Charles_I
    type: :Person
  AssignClass (63beb2e0-286b-43bb-893b-f32a2ba4a4a3)
 Call ID: 63beb2e0-286b-43bb-893b-f32a2ba4a4a3
  Args:
    source: Charles_I
    type: :Ancestor
  AddTriple (00e8c22e-1bf1-44a3-9dc2-f47980eb24a4)
 Call ID: 00e8c22e-1bf1-44a3-9dc2-f47980eb24a4
  Args:
    target: Charles_I
    source: Walburga_Douglas
    relation: :hasAncestor
  AssignClass (1a8024ee-e839-4e90-b466-2bd5455cf463)
 Call ID: 1a8024ee-e839-4e90-b466-2bd5455cf463
  Args:
    source: Carl_Axel_Archibald_Douglas
    type: :Man
  AssignClass (014dc9de-05d5-4049-b23f-1044228cf4e1)
 Call ID: 014dc9de-05d5-4049-b23f-1044228cf4e1
  Args:
    source: Carl_Axel_Archibald_Douglas
    type: :Person
  AddLiteral (f06068a7-e843-40bc-bb12-f2588ab7dc60)
 Call ID: f06068a7-e843-40bc-bb12-f2588ab7dc60
  Args:
    source: Carl_Axel_Archibald_Douglas
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1949
  AddLiteral (36e6db92-2cdf-45ef-8c67-f741a00d3829)
 Call ID: 36e6db92-2cdf-45ef-8c67-f741a00d3829
  Args:
    relation: :hasMarriageYear
    literal_value: 1992
    source: Walburga_Douglas
    literal_type: xsd:integer
  AddTriple (0fb2e3ff-18ea-4e8c-a7f7-e9b05f466cb6)
 Call ID: 0fb2e3ff-18ea-4e8c-a7f7-e9b05f466cb6
  Args:
    target: Carl_Axel_Archibald_Douglas
    source: Walburga_Douglas
    relation: :hasRelation
  AssignClass (988b08f3-8163-4747-9591-4de2f3ab7ed3)
 Call ID: 988b08f3-8163-4747-9591-4de2f3ab7ed3
  Args:
    source: Archibald_Douglas
    type: :Man
  AssignClass (3aa727e4-7e32-4e51-9fe2-9f5d842cf85c)
 Call ID: 3aa727e4-7e32-4e51-9fe2-9f5d842cf85c
  Args:
    source: Archibald_Douglas
    type: :Person
  AssignClass (9d6f47ba-caea-49b0-9d73-ce3e1a69227b)
 Call ID: 9d6f47ba-caea-49b0-9d73-ce3e1a69227b
  Args:
    source: Archibald_Douglas
    type: :Ancestor
  AssignClass (3bcb2bf9-4be8-4b94-b0c7-95b6ab505056)
 Call ID: 3bcb2bf9-4be8-4b94-b0c7-95b6ab505056
  Args:
    source: Margareta_Lagerfelt
    type: :Woman
  AssignClass (c71e494a-3676-410e-a8f9-d52d1b0f12d8)
 Call ID: c71e494a-3676-410e-a8f9-d52d1b0f12d8
  Args:
    source: Margareta_Lagerfelt
    type: :Person
  AssignClass (4b96ca91-f041-44d9-9421-951f13f7355e)
 Call ID: 4b96ca91-f041-44d9-9421-951f13f7355e
  Args:
    source: Margareta_Lagerfelt
    type: :Ancestor
  AddTriple (e209df9f-d680-49ee-b65c-994e0c36e40b)
 Call ID: e209df9f-d680-49ee-b65c-994e0c36e40b
  Args:
    relation: :hasFather
    source: Carl_Axel_Archibald_Douglas
    target: Archibald_Douglas
  AddTriple (27f25ad1-7d55-45a2-b63b-1845a13ecb0b)
 Call ID: 27f25ad1-7d55-45a2-b63b-1845a13ecb0b
  Args:
    source: Carl_Axel_Archibald_Douglas
    relation: :hasMother
    target: Margareta_Lagerfelt
  AssignClass (9a472d4a-9bbf-4939-accd-2dca9069a8c4)
 Call ID: 9a472d4a-9bbf-4939-accd-2dca9069a8c4
  Args:
    source: Mauritz_Otto_Wenzel_Douglas
    type: :Man
  AssignClass (1e24831f-6b29-45c9-a8d9-5101fff05d65)
 Call ID: 1e24831f-6b29-45c9-a8d9-5101fff05d65
  Args:
    source: Mauritz_Otto_Wenzel_Douglas
    type: :Person
  AddLiteral (ce1ac4b5-ac2e-484b-bf6b-3678664ef94b)
 Call ID: ce1ac4b5-ac2e-484b-bf6b-3678664ef94b
  Args:
    source: Mauritz_Otto_Wenzel_Douglas
    literal_type: xsd:integer
    literal_value: 1994
    relation: :hasBirthYear
  AddTriple (331087bd-91fe-488d-b98f-0943e7950cf9)
 Call ID: 331087bd-91fe-488d-b98f-0943e7950cf9
  Args:
    target: Carl_Axel_Archibald_Douglas
    source: Mauritz_Otto_Wenzel_Douglas
    relation: :hasFather
  AddTriple (7acecff1-d7ca-421d-ac50-fae8ecf7fdf1)
 Call ID: 7acecff1-d7ca-421d-ac50-fae8ecf7fdf1
  Args:
    target: Walburga_Douglas
    relation: :hasMother
    source: Mauritz_Otto_Wenzel_Douglas
  Finish (49b9f8e3-3877-4e1b-88aa-180fe7e88afd)
 Call ID: 49b9f8e3-3877-4e1b-88aa-180fe7e88afd
  Args: