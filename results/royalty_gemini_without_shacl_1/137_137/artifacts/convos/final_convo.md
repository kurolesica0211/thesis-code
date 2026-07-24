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
Lord Leopold Arthur Louis Mountbatten (21 May 1889 – 23 April 1922) was a British Army officer and a descendant of the Hessian princely Battenberg family and the British royal family.
A grandson of Queen Victoria, he was known as Prince Leopold of Battenberg from his birth until 1917, when the British royal family relinquished their German titles during World War I, and the Battenberg family changed their name to Mountbatten.
Early life

Leopold was born on 21 May 1889.
His father was Prince Henry of Battenberg, the son of Prince Alexander of Hesse and by Rhine and Julia, Princess of Battenberg.
His mother was Princess Beatrice of the United Kingdom, the fifth daughter and the youngest child of Queen Victoria and Prince Albert.
As he was the product of a morganatic marriage, Prince Henry of Battenberg took his style of Prince of Battenberg from his mother, Julia von Hauke, who was created Princess of Battenberg in her own right.
As such, Leopold was styled as His Serene Highness Prince Leopold of Battenberg from birth.
In the United Kingdom, he was styled His Highness Prince Leopold of Battenberg under a royal warrant passed by Queen Victoria in 1886.
His godparents were Leopold II of Belgium (his first cousin twice removed, represented by the Prince of Wales, his maternal uncle), the Duke of Connaught and Strathearn (his maternal uncle, represented by Prince Albert of Schleswig-Holstein, his first cousin), Prince Louis of Battenberg (his paternal uncle, represented by the Marquess of Lorne, his maternal uncle), the Marchioness of Lorne (his maternal aunt), the Duchess of Albany (his maternal aunt) and Princess Marie of Erbach-Schönberg (his paternal aunt).
Leopold was a haemophiliac, a condition he inherited through his mother.
His namesake maternal uncle, Prince Leopold, Duke of Albany, had died from the same condition.
Military career

Leopold was commissioned a lieutenant (supernumerary) on 16 October 1909 in the 8th Battalion of the Isle of Wight Rifles, a Territorial Force unit.
Relinquishment of titles

During the First World War, anti-German feeling in the United Kingdom led Leopold's first cousin, George V to change the name of the royal house from the Germanic House of Saxe-Coburg and Gotha to the more English-sounding House of Windsor.
In response to this, Leopold renounced his title of Prince, the style His Highness and the designation 'of Battenberg' through a royal warrant from the King dated 14 July 1917, and became Sir Leopold Mountbatten by virtue of his being a Knight Grand Cross of the Royal Victorian Order.
Under a further warrant of 11 September 1917 he was granted the style and precedence of the younger son of a marquess, and became Lord Leopold Mountbatten.
Death

Lord Leopold died on 23 April 1922(1922-04-23) (aged 32), during a hip operation.



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
  AssignClass (32cc5b71-8680-42dc-97b8-b77fa0c00bd0)
 Call ID: 32cc5b71-8680-42dc-97b8-b77fa0c00bd0
  Args:
    source: Leopold_Mountbatten
    type: :Man
  AssignClass (da1575fe-80bc-440b-931f-a7229ed97d76)
 Call ID: da1575fe-80bc-440b-931f-a7229ed97d76
  Args:
    source: Leopold_Mountbatten
    type: :Person
  AddLiteral (f34b9221-f7da-4715-90c5-d62e1419f5a7)
 Call ID: f34b9221-f7da-4715-90c5-d62e1419f5a7
  Args:
    literal_type: xsd:string
    source: Leopold_Mountbatten
    literal_value: Lord Leopold Arthur Louis Mountbatten
    relation: :knownAs
  AddLiteral (2ac63f40-a141-499c-bf8a-c3aaeacc9382)
 Call ID: 2ac63f40-a141-499c-bf8a-c3aaeacc9382
  Args:
    literal_type: xsd:integer
    source: Leopold_Mountbatten
    literal_value: 1889
    relation: :hasBirthYear
  AddLiteral (fec7bdf5-91d4-423f-9600-c7ba13296164)
 Call ID: fec7bdf5-91d4-423f-9600-c7ba13296164
  Args:
    literal_type: xsd:integer
    source: Leopold_Mountbatten
    literal_value: 1922
    relation: :hasDeathYear
  AssignClass (94dd291e-cada-4cd4-ab20-59b2a6cd59d1)
 Call ID: 94dd291e-cada-4cd4-ab20-59b2a6cd59d1
  Args:
    source: Henry_of_Battenberg
    type: :Man
  AssignClass (0d0a27c7-692d-4a63-b6d5-ea8c41a2b742)
 Call ID: 0d0a27c7-692d-4a63-b6d5-ea8c41a2b742
  Args:
    type: :Person
    source: Henry_of_Battenberg
  AddTriple (c947312c-e087-446c-89c1-deb8bd11ee97)
 Call ID: c947312c-e087-446c-89c1-deb8bd11ee97
  Args:
    relation: :hasFather
    target: Henry_of_Battenberg
    source: Leopold_Mountbatten
  AssignClass (775c0606-85dd-4ee0-bf46-dbdfd36bb1fa)
 Call ID: 775c0606-85dd-4ee0-bf46-dbdfd36bb1fa
  Args:
    source: Beatrice_of_the_United_Kingdom
    type: :Woman
  AssignClass (fe46c82e-463a-46b9-a76e-6982642b6827)
 Call ID: fe46c82e-463a-46b9-a76e-6982642b6827
  Args:
    type: :Person
    source: Beatrice_of_the_United_Kingdom
  AddTriple (a6d0aac4-be6f-4311-9e7e-e95684af607c)
 Call ID: a6d0aac4-be6f-4311-9e7e-e95684af607c
  Args:
    relation: :hasMother
    source: Leopold_Mountbatten
    target: Beatrice_of_the_United_Kingdom
  AssignClass (1e906f5d-1533-4a87-a7b2-1994ff510e00)
 Call ID: 1e906f5d-1533-4a87-a7b2-1994ff510e00
  Args:
    source: Alexander_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (b731bd88-a72f-4e96-9ea2-b9638bb935a0)
 Call ID: b731bd88-a72f-4e96-9ea2-b9638bb935a0
  Args:
    type: :Person
    source: Alexander_of_Hesse_and_by_Rhine
  AddTriple (279bcc40-1010-49c4-a9cf-8d208481d1ae)
 Call ID: 279bcc40-1010-49c4-a9cf-8d208481d1ae
  Args:
    relation: :hasFather
    target: Alexander_of_Hesse_and_by_Rhine
    source: Henry_of_Battenberg
  AssignClass (37272f42-45fb-4d0b-9d43-bfa79eff9277)
 Call ID: 37272f42-45fb-4d0b-9d43-bfa79eff9277
  Args:
    source: Julia_Princess_of_Battenberg
    type: :Woman
  AssignClass (888d8bfe-e752-43de-af18-c2a509db89ff)
 Call ID: 888d8bfe-e752-43de-af18-c2a509db89ff
  Args:
    source: Julia_Princess_of_Battenberg
    type: :Person
  AddTriple (c896ced7-aae3-457b-8f62-77f7bad41053)
 Call ID: c896ced7-aae3-457b-8f62-77f7bad41053
  Args:
    relation: :hasMother
    source: Henry_of_Battenberg
    target: Julia_Princess_of_Battenberg
  AssignClass (27961564-8aa8-45a7-87ae-70bfa5720f70)
 Call ID: 27961564-8aa8-45a7-87ae-70bfa5720f70
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (bacc3cc4-bc46-4bdf-b6d7-6d2d2fbcdbe5)
 Call ID: bacc3cc4-bc46-4bdf-b6d7-6d2d2fbcdbe5
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (292081cd-e12d-411b-a025-aeb8cba2299c)
 Call ID: 292081cd-e12d-411b-a025-aeb8cba2299c
  Args:
    relation: :hasMother
    source: Beatrice_of_the_United_Kingdom
    target: Queen_Victoria
  AssignClass (bdb7fb07-426c-4dc6-a8e1-514934c9ad98)
 Call ID: bdb7fb07-426c-4dc6-a8e1-514934c9ad98
  Args:
    source: Prince_Albert
    type: :Man
  AssignClass (c1b805a5-6b5d-4120-9c60-3a56ec177407)
 Call ID: c1b805a5-6b5d-4120-9c60-3a56ec177407
  Args:
    type: :Person
    source: Prince_Albert
  AddTriple (795823b2-fff3-4764-950e-dfcde3c56e20)
 Call ID: 795823b2-fff3-4764-950e-dfcde3c56e20
  Args:
    target: Prince_Albert
    source: Beatrice_of_the_United_Kingdom
    relation: :hasFather
  Finish (780c7c3b-61e2-48b3-8e3a-5ee58b319403)
 Call ID: 780c7c3b-61e2-48b3-8e3a-5ee58b319403
  Args: