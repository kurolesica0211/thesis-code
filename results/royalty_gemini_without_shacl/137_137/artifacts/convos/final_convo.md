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
  AssignClass (bebf2a42-77da-4308-859c-28c9b174d695)
 Call ID: bebf2a42-77da-4308-859c-28c9b174d695
  Args:
    type: :Person
    source: Leopold_Mountbatten
  AssignClass (96c9e9de-dc8b-458a-b927-1fef8925fb99)
 Call ID: 96c9e9de-dc8b-458a-b927-1fef8925fb99
  Args:
    source: Leopold_Mountbatten
    type: :Man
  AddLiteral (cb2ca94d-3f36-4fcc-8b5e-6836ef896895)
 Call ID: cb2ca94d-3f36-4fcc-8b5e-6836ef896895
  Args:
    literal_value: 1889
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Leopold_Mountbatten
  AddLiteral (acaf44bb-15a5-479a-a765-b88ae24b5e66)
 Call ID: acaf44bb-15a5-479a-a765-b88ae24b5e66
  Args:
    literal_value: 1922
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Leopold_Mountbatten
  AssignClass (e67a46ba-90cd-48b3-9a73-0772328d2bee)
 Call ID: e67a46ba-90cd-48b3-9a73-0772328d2bee
  Args:
    type: :Person
    source: Henry_of_Battenberg
  AssignClass (eca90329-58f4-4978-876a-969a2c9193b8)
 Call ID: eca90329-58f4-4978-876a-969a2c9193b8
  Args:
    source: Henry_of_Battenberg
    type: :Man
  AssignClass (c1771311-12e3-48e1-a9b4-647a96d2f8e2)
 Call ID: c1771311-12e3-48e1-a9b4-647a96d2f8e2
  Args:
    source: Alexander_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (f351c1ca-0b80-4540-9468-fae26a53da79)
 Call ID: f351c1ca-0b80-4540-9468-fae26a53da79
  Args:
    source: Alexander_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (18dde873-95c9-480d-ac61-da4ca02499de)
 Call ID: 18dde873-95c9-480d-ac61-da4ca02499de
  Args:
    source: Julia_Princess_of_Battenberg
    type: :Person
  AssignClass (cd5c66ea-8b9d-44ce-8eec-604d31deeb00)
 Call ID: cd5c66ea-8b9d-44ce-8eec-604d31deeb00
  Args:
    source: Julia_Princess_of_Battenberg
    type: :Woman
  AssignClass (91943bd1-8720-43d8-9c5a-46de4efec68c)
 Call ID: 91943bd1-8720-43d8-9c5a-46de4efec68c
  Args:
    source: Beatrice_of_the_United_Kingdom
    type: :Person
  AssignClass (927f8c19-ed0a-46a1-a885-5b3dea0edb3c)
 Call ID: 927f8c19-ed0a-46a1-a885-5b3dea0edb3c
  Args:
    source: Beatrice_of_the_United_Kingdom
    type: :Woman
  AssignClass (34be8cf5-ce5a-4353-81f1-95f521572952)
 Call ID: 34be8cf5-ce5a-4353-81f1-95f521572952
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (db0609e0-9492-47ef-bbc9-f5754aad99ab)
 Call ID: db0609e0-9492-47ef-bbc9-f5754aad99ab
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (6a61c74a-9da5-47d3-8bec-3c56c09207ab)
 Call ID: 6a61c74a-9da5-47d3-8bec-3c56c09207ab
  Args:
    source: Prince_Albert
    type: :Person
  AssignClass (c64ae4fe-f51f-454f-94bc-1fb39b3089fe)
 Call ID: c64ae4fe-f51f-454f-94bc-1fb39b3089fe
  Args:
    type: :Man
    source: Prince_Albert
  AddTriple (f6456f6d-6633-4157-a4d6-73f297497049)
 Call ID: f6456f6d-6633-4157-a4d6-73f297497049
  Args:
    source: Leopold_Mountbatten
    relation: :hasFather
    target: Henry_of_Battenberg
  AddTriple (f768deb3-2171-4f6b-83b4-43f6e0c1e790)
 Call ID: f768deb3-2171-4f6b-83b4-43f6e0c1e790
  Args:
    source: Leopold_Mountbatten
    target: Beatrice_of_the_United_Kingdom
    relation: :hasMother
  AddTriple (f1a704cc-9c7d-4b57-8c4f-664d4a85db66)
 Call ID: f1a704cc-9c7d-4b57-8c4f-664d4a85db66
  Args:
    target: Alexander_of_Hesse_and_by_Rhine
    relation: :hasFather
    source: Henry_of_Battenberg
  AddTriple (e73ea72b-3604-4e58-a11e-98e86f76d5ed)
 Call ID: e73ea72b-3604-4e58-a11e-98e86f76d5ed
  Args:
    target: Julia_Princess_of_Battenberg
    relation: :hasMother
    source: Henry_of_Battenberg
  AddTriple (fc34ebf3-0de8-428d-86a9-7c615e8ba43c)
 Call ID: fc34ebf3-0de8-428d-86a9-7c615e8ba43c
  Args:
    target: Prince_Albert
    relation: :hasFather
    source: Beatrice_of_the_United_Kingdom
  AddTriple (8604698d-f425-44ca-b2a8-aae5d9153100)
 Call ID: 8604698d-f425-44ca-b2a8-aae5d9153100
  Args:
    target: Queen_Victoria
    relation: :hasMother
    source: Beatrice_of_the_United_Kingdom
  Finish (73abd79f-ed12-4cad-9d0e-8276a37c4bc4)
 Call ID: 73abd79f-ed12-4cad-9d0e-8276a37c4bc4
  Args: