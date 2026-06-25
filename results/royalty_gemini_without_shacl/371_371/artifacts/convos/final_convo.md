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
Duke John Albert of Mecklenburg (German: Herzog Johann Albrecht zu Mecklenburg; given names John Albert Ernest Constantine Frederick Henry; 8 December 1857 – 16 February 1920) was a member of the House of Mecklenburg-Schwerin who served as the regent of two states of the German Empire.
He was first regent of the Grand Duchy of Mecklenburg-Schwerin from 1897 to 1901 for his nephew Frederick Francis IV, Grand Duke of Mecklenburg, and thereafter regent of the Duchy of Brunswick from 1907 to 1913.
Birth and interests

Duke John Albert of Mecklenburg was born in Schwerin the fifth child of Frederick Francis II, Grand Duke of Mecklenburg and his first wife Princess Augusta Reuss of Köstritz (1822–1862).
Duke John Albert was educated in Dresden, pursued a career in the Prussian Army and was well known for his love of sports.
Regencies

Following the death of his brother Frederick Francis III, Grand Duke of Mecklenburg on 10 April 1897, Duke John Albert was appointed regent for his young nephew the new Grand Duke, Frederick Francis IV after his older brother Duke Paul Frederick had renounced his claim to the regency.
On 28 May 1907, Duke John Albert was elected regent of the Duchy of Brunswick following the death of Prince Albert of Prussia by the state's diet, accepting the offer he arrived in Brunswick on 5 June 1907.
The reason for the regency in Brunswick was that in 1884 when William, Duke of Brunswick died his distant cousin and heir Ernest Augustus, Crown Prince of Hanover was prevented from taking over the duchy because he refused to renounce his claim to the throne of the Kingdom of Hanover which had been annexed by Prussia in 1866.
Shortly after assuming the regency, Duke John Albert would walk Brunswick in civilian clothes visiting museums, libraries and other institutions in the duchy, asking questions of people to discover their living conditions.
Duke John Albert also cut down on the expenses of the royal household by cutting the number of servants and retainers to the minimum needed to run the household.
The regency came to an end on 1 November 1913 when Ernest Augustus, Crown Prince of Hanover's son Ernest Augustus was permitted to ascend to Duchy following his marriage to Princess Victoria Louise of Prussia, the only daughter of the German Emperor, William II, which helped heal the rift between the houses of Hanover and Hohenzollern.
War years

During the First World War, Duke John Albert was active with the German Colonial Society in defending Germany's colonial possessions from suggestions that they should be abandoned.
Duke John Albert died in 1920 in Wiligrad castle near Lübstorf aged 62.
Marriages

John Albert was married twice: firstly in Weimar on 6 November 1886 to Princess Elisabeth Sybille of Saxe-Weimar-Eisenach (28 February 1854–10 July 1908)
the daughter of Charles Alexander, Grand Duke of Saxe-Weimar-Eisenach; secondly in Brunswick on 15 December 1909 to Princess Elisabeth of Stolberg-Rossla (1885–1969), who following his death was to marry his half brother Duke Adolf Friedrich in 1924.
Ojimukoka

Ojimukoka, a small settlement, postoffice and railway station in Namibia, was renamed Johann - Albrechtshöhe, and then simply Albrechts in his honour.



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
  AssignClass (b2e85307-b272-48ce-a065-0651171c9727)
 Call ID: b2e85307-b272-48ce-a065-0651171c9727
  Args:
    source: John_Albert_of_Mecklenburg
    type: :Man
  AssignClass (392fc95d-e178-4055-9422-1bd9c3e4dbbc)
 Call ID: 392fc95d-e178-4055-9422-1bd9c3e4dbbc
  Args:
    source: John_Albert_of_Mecklenburg
    type: :Person
  AddLiteral (6d89d619-fcae-4581-bc17-52a14d14f85d)
 Call ID: 6d89d619-fcae-4581-bc17-52a14d14f85d
  Args:
    literal_value: 1857
    relation: :hasBirthYear
    source: John_Albert_of_Mecklenburg
    literal_type: xsd:integer
  AddLiteral (bdc0cbf1-1268-4c0d-a9f6-5df189893fb2)
 Call ID: bdc0cbf1-1268-4c0d-a9f6-5df189893fb2
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: John_Albert_of_Mecklenburg
    literal_value: 1920
  AssignClass (a1324665-e46e-4f4d-9546-e300cc6988f9)
 Call ID: a1324665-e46e-4f4d-9546-e300cc6988f9
  Args:
    source: Frederick_Francis_II
    type: :Man
  AssignClass (22397cd1-80b9-4956-830f-0d2885d258c3)
 Call ID: 22397cd1-80b9-4956-830f-0d2885d258c3
  Args:
    source: Frederick_Francis_II
    type: :Person
  AssignClass (fead0d16-a140-462f-9fd0-f73c082b8750)
 Call ID: fead0d16-a140-462f-9fd0-f73c082b8750
  Args:
    source: Augusta_Reuss_of_Köstritz
    type: :Woman
  AssignClass (b0d620b6-0a80-4991-9971-ca55ae9540b8)
 Call ID: b0d620b6-0a80-4991-9971-ca55ae9540b8
  Args:
    source: Augusta_Reuss_of_Köstritz
    type: :Person
  AddTriple (32219036-d23a-4dae-afb8-953d791f820e)
 Call ID: 32219036-d23a-4dae-afb8-953d791f820e
  Args:
    target: Frederick_Francis_II
    source: John_Albert_of_Mecklenburg
    relation: :hasFather
  AddTriple (723c8ba6-cd00-405c-b848-97515f210974)
 Call ID: 723c8ba6-cd00-405c-b848-97515f210974
  Args:
    source: John_Albert_of_Mecklenburg
    relation: :hasMother
    target: Augusta_Reuss_of_Köstritz
  AssignClass (2d632332-c700-4691-9018-82797ae80ec7)
 Call ID: 2d632332-c700-4691-9018-82797ae80ec7
  Args:
    source: Frederick_Francis_III
    type: :Man
  AssignClass (39463c8c-2fa5-4769-bef5-6c901ee47071)
 Call ID: 39463c8c-2fa5-4769-bef5-6c901ee47071
  Args:
    source: Frederick_Francis_III
    type: :Person
  AddTriple (bcd88f98-8c6a-4eb9-8a8e-3b43c9cc905f)
 Call ID: bcd88f98-8c6a-4eb9-8a8e-3b43c9cc905f
  Args:
    relation: :isBrotherOf
    source: John_Albert_of_Mecklenburg
    target: Frederick_Francis_III
  AssignClass (a0c35d55-083d-4819-9884-e163f59baabe)
 Call ID: a0c35d55-083d-4819-9884-e163f59baabe
  Args:
    source: Paul_Frederick
    type: :Man
  AssignClass (99d2a860-4eb0-417f-b9b4-f53427cbf31d)
 Call ID: 99d2a860-4eb0-417f-b9b4-f53427cbf31d
  Args:
    source: Paul_Frederick
    type: :Person
  AddTriple (da3621ee-1dc0-4ef3-918e-237cfcaf2dfc)
 Call ID: da3621ee-1dc0-4ef3-918e-237cfcaf2dfc
  Args:
    relation: :isBrotherOf
    source: John_Albert_of_Mecklenburg
    target: Paul_Frederick
  AssignClass (15802c4e-aae6-478a-b5c6-08d7b927e4db)
 Call ID: 15802c4e-aae6-478a-b5c6-08d7b927e4db
  Args:
    source: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
    type: :Woman
  AssignClass (b0ee8799-c5d0-4ddc-8a40-0a80a8c732f5)
 Call ID: b0ee8799-c5d0-4ddc-8a40-0a80a8c732f5
  Args:
    source: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
    type: :Person
  AddLiteral (39daa00f-875a-4bc2-963a-93e950741197)
 Call ID: 39daa00f-875a-4bc2-963a-93e950741197
  Args:
    source: John_Albert_of_Mecklenburg
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1886
  AssignClass (1b89cf02-f931-4823-bdec-5016256e7ad4)
 Call ID: 1b89cf02-f931-4823-bdec-5016256e7ad4
  Args:
    source: Elisabeth_of_Stolberg-Rossla
    type: :Woman
  AssignClass (aea8d7a6-91cd-46d6-bcf8-3df9d8a4faa2)
 Call ID: aea8d7a6-91cd-46d6-bcf8-3df9d8a4faa2
  Args:
    source: Elisabeth_of_Stolberg-Rossla
    type: :Person
  AddLiteral (4b02e12f-b45d-4865-9b08-4f99a20fdb68)
 Call ID: 4b02e12f-b45d-4865-9b08-4f99a20fdb68
  Args:
    literal_value: 1909
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: John_Albert_of_Mecklenburg
  AssignClass (c5425156-0a91-4f24-aa67-0ff4d9a3cc72)
 Call ID: c5425156-0a91-4f24-aa67-0ff4d9a3cc72
  Args:
    source: Adolf_Friedrich
    type: :Man
  AssignClass (52721585-43c0-4261-ae04-2f9a6333e49b)
 Call ID: 52721585-43c0-4261-ae04-2f9a6333e49b
  Args:
    source: Adolf_Friedrich
    type: :Person
  Finish (62cf3f04-adfe-47bc-81b5-823f5a1f813a)
 Call ID: 62cf3f04-adfe-47bc-81b5-823f5a1f813a
  Args: