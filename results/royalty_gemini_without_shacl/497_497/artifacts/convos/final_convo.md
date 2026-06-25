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
Ferdinand d'Orléans, Duke of Montpensier (French: Ferdinand François Philippe Marie Laurent d'Orléans, Duc de Montpensier) (9 September 1884 – 30 January 1924) was a member of the House of Orléans and a Prince of France.
Early life

Ferdinand was born on 9 September 1884 at Château d'Eu, Eu, Seine-Inférieure, French Republic.
He was the eighth, and youngest, child of Philippe d'Orléans, Count of Paris and his wife Marie Isabelle d'Orléans.
His elder siblings were Princess Amélie (wife of Carlos I of Portugal), Prince Philippe (who married Archduchess Maria Dorothea, daughter of Archduke Joseph Karl of Austria), Princess Hélène (the wife of Emmanuel Philibert, 2nd Duke of Aosta), Prince Charles (who died young), Princess Isabelle (wife of Prince Jean D'Orléans, Duke of Guise), Prince Jacques (who also died young), and Princess Louise (wife of Prince Carlos of Bourbon-Two Sicilies).
His paternal grandparents were Prince Ferdinand, Duke of Orléans and Duchess Helene of Mecklenburg-Schwerin.
Through his father, he was a great-grandson of Louis-Philippe I, King of the French and his wife Queen Maria Amalia of the Two Sicilies.
His maternal grandparents were Infanta Luisa Fernanda of Spain and Prince Antoine, Duke of Montpensier (the youngest son of Louis-Philippe of France and Maria Amalia of Naples and Sicily).
Career

The Duke lived in England for many years, until "his reported indiscretions with regard to his recollections of Queen Victoria made it somewhat uncomfortable for him when in London."
Others considered for the throne were Prince Ghika of Romania, Prince Karl, Duke of Urach, Prince Moritz of Schaumburg-Lippe, Prince Vittorio Emanuele, Count of Turin and Prince Arthur of Connaught.
Personal life

On 20 August 1921, Ferdinand married Doña María Isabel González de Olañeta e Ibarreta (22 April 1895 – 11 July 1958), 3rd Marchioness of Valdeterrazo and Grandee of Spain, 2nd
She was the daughter of Don Ulpiano González de Olañeta y González de Ocampo, 2nd Marquis of Valdeterrazo and Grandee of Spain, and his wife Doña Isabel de Ibarreta y Uhagón.
Ferdinand and María Isabel did not have children.
The Duke of Montpensier died on 30 January 1924 at the Château de Randan in Randan in the French Republic.



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
  AssignClass (a9bc54f9-2b7d-4576-acce-ba7265fe5883)
 Call ID: a9bc54f9-2b7d-4576-acce-ba7265fe5883
  Args:
    type: :Man
    source: Ferdinand_dOrleans
  AssignClass (4d4a73c1-93f0-42eb-ad93-bcb9bf418bde)
 Call ID: 4d4a73c1-93f0-42eb-ad93-bcb9bf418bde
  Args:
    type: :Person
    source: Ferdinand_dOrleans
  AddLiteral (3509fb16-a807-40f2-a279-2d9354f64325)
 Call ID: 3509fb16-a807-40f2-a279-2d9354f64325
  Args:
    literal_type: xsd:integer
    literal_value: 1884
    source: Ferdinand_dOrleans
    relation: :hasBirthYear
  AddLiteral (7e424b2f-4c97-4c8a-b3c1-1380826178a7)
 Call ID: 7e424b2f-4c97-4c8a-b3c1-1380826178a7
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1924
    source: Ferdinand_dOrleans
  AssignClass (26ba6e3e-df4f-4e2f-94ab-5c71bef17f69)
 Call ID: 26ba6e3e-df4f-4e2f-94ab-5c71bef17f69
  Args:
    type: :Man
    source: Philippe_dOrleans_Count_of_Paris
  AssignClass (8e38dec1-f8dd-47ab-98ba-38a8755f1ff6)
 Call ID: 8e38dec1-f8dd-47ab-98ba-38a8755f1ff6
  Args:
    type: :Person
    source: Philippe_dOrleans_Count_of_Paris
  AssignClass (2fb12106-b3d8-4d51-b24c-7139b998dde5)
 Call ID: 2fb12106-b3d8-4d51-b24c-7139b998dde5
  Args:
    source: Marie_Isabelle_dOrleans
    type: :Woman
  AssignClass (4e1f309b-033d-4e99-83c8-51fb901f8acf)
 Call ID: 4e1f309b-033d-4e99-83c8-51fb901f8acf
  Args:
    source: Marie_Isabelle_dOrleans
    type: :Person
  AddTriple (482e5818-4b80-4b61-bc85-d80abff2879c)
 Call ID: 482e5818-4b80-4b61-bc85-d80abff2879c
  Args:
    relation: :hasFather
    source: Ferdinand_dOrleans
    target: Philippe_dOrleans_Count_of_Paris
  AddTriple (925d9b76-a9fd-40e7-acb1-c985bd5f084c)
 Call ID: 925d9b76-a9fd-40e7-acb1-c985bd5f084c
  Args:
    relation: :hasMother
    source: Ferdinand_dOrleans
    target: Marie_Isabelle_dOrleans
  AssignClass (f3b1c13d-7bc6-43da-a820-1128e105040e)
 Call ID: f3b1c13d-7bc6-43da-a820-1128e105040e
  Args:
    type: :Woman
    source: Princess_Amelie
  AssignClass (3cd90ad6-1163-42ae-936d-970711588d85)
 Call ID: 3cd90ad6-1163-42ae-936d-970711588d85
  Args:
    type: :Person
    source: Princess_Amelie
  AssignClass (794e201f-1c0c-45be-8803-11817882e526)
 Call ID: 794e201f-1c0c-45be-8803-11817882e526
  Args:
    source: Prince_Philippe
    type: :Man
  AssignClass (fc9503c9-d07e-4133-bae8-1cefb954494b)
 Call ID: fc9503c9-d07e-4133-bae8-1cefb954494b
  Args:
    type: :Person
    source: Prince_Philippe
  AssignClass (6c83ab19-5b18-411e-ac65-7b21799aeb52)
 Call ID: 6c83ab19-5b18-411e-ac65-7b21799aeb52
  Args:
    type: :Woman
    source: Princess_Helene
  AssignClass (dadf7614-aaaf-45bb-9145-b64dafa0f3e5)
 Call ID: dadf7614-aaaf-45bb-9145-b64dafa0f3e5
  Args:
    source: Princess_Helene
    type: :Person
  AssignClass (3045826f-c534-46fa-9243-191dc1321544)
 Call ID: 3045826f-c534-46fa-9243-191dc1321544
  Args:
    type: :Man
    source: Prince_Charles
  AssignClass (e8df4aaa-24c2-42fa-aec0-fd3ea48ea6b5)
 Call ID: e8df4aaa-24c2-42fa-aec0-fd3ea48ea6b5
  Args:
    source: Prince_Charles
    type: :Person
  AssignClass (d79a49cb-bafc-4a3c-8b90-67d77ea8a50b)
 Call ID: d79a49cb-bafc-4a3c-8b90-67d77ea8a50b
  Args:
    type: :Woman
    source: Princess_Isabelle
  AssignClass (5fd641c9-6268-4dbe-9af4-26804af606d0)
 Call ID: 5fd641c9-6268-4dbe-9af4-26804af606d0
  Args:
    source: Princess_Isabelle
    type: :Person
  AssignClass (454115b2-5ab0-4f2f-b63b-62ceaa86386f)
 Call ID: 454115b2-5ab0-4f2f-b63b-62ceaa86386f
  Args:
    type: :Man
    source: Prince_Jacques
  AssignClass (33c2cfb5-214c-492e-8858-cbb609a62a92)
 Call ID: 33c2cfb5-214c-492e-8858-cbb609a62a92
  Args:
    type: :Person
    source: Prince_Jacques
  AssignClass (fc90735b-b15d-4a3f-802e-7718b3cbe3f9)
 Call ID: fc90735b-b15d-4a3f-802e-7718b3cbe3f9
  Args:
    source: Princess_Louise
    type: :Woman
  AssignClass (65431b58-4166-4979-b5b2-b9ca8cfb6182)
 Call ID: 65431b58-4166-4979-b5b2-b9ca8cfb6182
  Args:
    type: :Person
    source: Princess_Louise
  AddTriple (794cf50e-bee8-48b4-9f32-3bd4b9089602)
 Call ID: 794cf50e-bee8-48b4-9f32-3bd4b9089602
  Args:
    target: Princess_Amelie
    source: Ferdinand_dOrleans
    relation: :isSiblingOf
  AddTriple (767ba636-2c1a-4f04-8b32-acd16a7604a8)
 Call ID: 767ba636-2c1a-4f04-8b32-acd16a7604a8
  Args:
    target: Prince_Philippe
    source: Ferdinand_dOrleans
    relation: :isSiblingOf
  AddTriple (b3e82b2a-ffed-4dcf-9736-294ce31a4465)
 Call ID: b3e82b2a-ffed-4dcf-9736-294ce31a4465
  Args:
    source: Ferdinand_dOrleans
    target: Princess_Helene
    relation: :isSiblingOf
  AddTriple (7272f67a-cdd0-4cf3-80a4-5871dcc77e82)
 Call ID: 7272f67a-cdd0-4cf3-80a4-5871dcc77e82
  Args:
    relation: :isSiblingOf
    source: Ferdinand_dOrleans
    target: Prince_Charles
  AddTriple (78455d46-a090-4f72-9dd1-be5a9479392c)
 Call ID: 78455d46-a090-4f72-9dd1-be5a9479392c
  Args:
    target: Princess_Isabelle
    source: Ferdinand_dOrleans
    relation: :isSiblingOf
  AddTriple (72831962-5e9d-4459-bd13-2c434e3f1bd9)
 Call ID: 72831962-5e9d-4459-bd13-2c434e3f1bd9
  Args:
    source: Ferdinand_dOrleans
    target: Prince_Jacques
    relation: :isSiblingOf
  AddTriple (f9f7a155-4054-4695-9225-bdf069a52af6)
 Call ID: f9f7a155-4054-4695-9225-bdf069a52af6
  Args:
    target: Princess_Louise
    source: Ferdinand_dOrleans
    relation: :isSiblingOf
  AssignClass (08cc193a-f10e-4d1c-b68f-7d093b179fb3)
 Call ID: 08cc193a-f10e-4d1c-b68f-7d093b179fb3
  Args:
    type: :Man
    source: Prince_Ferdinand_Duke_of_Orleans
  AssignClass (f32f7c95-75a3-4fb9-a20a-16abff350f4f)
 Call ID: f32f7c95-75a3-4fb9-a20a-16abff350f4f
  Args:
    source: Prince_Ferdinand_Duke_of_Orleans
    type: :Person
  AssignClass (2f71f688-509e-4a24-972d-c42b03a603c0)
 Call ID: 2f71f688-509e-4a24-972d-c42b03a603c0
  Args:
    source: Duchess_Helene_of_Mecklenburg_Schwerin
    type: :Woman
  AssignClass (cdbabc7d-2310-47e6-b93a-f17b3eee11fc)
 Call ID: cdbabc7d-2310-47e6-b93a-f17b3eee11fc
  Args:
    source: Duchess_Helene_of_Mecklenburg_Schwerin
    type: :Person
  AddTriple (3d7eb9d4-8368-4e74-a4ea-1f0b0c5041d7)
 Call ID: 3d7eb9d4-8368-4e74-a4ea-1f0b0c5041d7
  Args:
    source: Philippe_dOrleans_Count_of_Paris
    target: Prince_Ferdinand_Duke_of_Orleans
    relation: :hasFather
  AddTriple (7fdf4db9-f482-4531-b53c-c52326eb9dd8)
 Call ID: 7fdf4db9-f482-4531-b53c-c52326eb9dd8
  Args:
    target: Duchess_Helene_of_Mecklenburg_Schwerin
    source: Philippe_dOrleans_Count_of_Paris
    relation: :hasMother
  AssignClass (fad92a87-77fd-4db1-913a-34dfea24d070)
 Call ID: fad92a87-77fd-4db1-913a-34dfea24d070
  Args:
    type: :Man
    source: Louis_Philippe_I
  AssignClass (8f107f76-cc2a-4da8-86e1-65935c803f4a)
 Call ID: 8f107f76-cc2a-4da8-86e1-65935c803f4a
  Args:
    source: Louis_Philippe_I
    type: :Person
  AssignClass (31783bc0-797b-43b3-b0a0-7be8de4316c8)
 Call ID: 31783bc0-797b-43b3-b0a0-7be8de4316c8
  Args:
    source: Queen_Maria_Amalia_of_the_Two_Sicilies
    type: :Woman
  AssignClass (c39c3ee6-4167-47f6-9a06-a37a674c421d)
 Call ID: c39c3ee6-4167-47f6-9a06-a37a674c421d
  Args:
    source: Queen_Maria_Amalia_of_the_Two_Sicilies
    type: :Person
  AddTriple (78d64baf-e6d5-428a-90d5-9c27b999edc0)
 Call ID: 78d64baf-e6d5-428a-90d5-9c27b999edc0
  Args:
    target: Louis_Philippe_I
    source: Prince_Ferdinand_Duke_of_Orleans
    relation: :hasFather
  AddTriple (add91c79-e717-4718-8685-951ec89a0c03)
 Call ID: add91c79-e717-4718-8685-951ec89a0c03
  Args:
    relation: :hasMother
    target: Queen_Maria_Amalia_of_the_Two_Sicilies
    source: Prince_Ferdinand_Duke_of_Orleans
  AssignClass (e108cb29-a4c3-4f43-be5f-2c1e578859a7)
 Call ID: e108cb29-a4c3-4f43-be5f-2c1e578859a7
  Args:
    source: Infanta_Luisa_Fernanda_of_Spain
    type: :Woman
  AssignClass (0ccc43df-b2c3-432b-91c9-d159168caec6)
 Call ID: 0ccc43df-b2c3-432b-91c9-d159168caec6
  Args:
    type: :Person
    source: Infanta_Luisa_Fernanda_of_Spain
  AssignClass (6f05dbc1-e62b-42b9-b61d-9fb6f0d456e9)
 Call ID: 6f05dbc1-e62b-42b9-b61d-9fb6f0d456e9
  Args:
    type: :Man
    source: Prince_Antoine_Duke_of_Montpensier
  AssignClass (d8234f6a-9150-480a-b919-86f1fd101d26)
 Call ID: d8234f6a-9150-480a-b919-86f1fd101d26
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    type: :Person
  AddTriple (24cef60e-6bc0-4326-b457-9f512352ef73)
 Call ID: 24cef60e-6bc0-4326-b457-9f512352ef73
  Args:
    relation: :hasMother
    source: Marie_Isabelle_dOrleans
    target: Infanta_Luisa_Fernanda_of_Spain
  AddTriple (5fcc38b7-9c8e-4237-9848-8fce1d1e4909)
 Call ID: 5fcc38b7-9c8e-4237-9848-8fce1d1e4909
  Args:
    target: Prince_Antoine_Duke_of_Montpensier
    source: Marie_Isabelle_dOrleans
    relation: :hasFather
  AssignClass (b89bc15f-1771-4fb5-ab8f-787e7ae146ba)
 Call ID: b89bc15f-1771-4fb5-ab8f-787e7ae146ba
  Args:
    type: :Woman
    source: Dona_Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AssignClass (306e92dd-6321-4642-bc37-c66901a06af8)
 Call ID: 306e92dd-6321-4642-bc37-c66901a06af8
  Args:
    type: :Person
    source: Dona_Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AddTriple (9ea02ec8-05a4-4bb4-99f5-6cbbf365adb0)
 Call ID: 9ea02ec8-05a4-4bb4-99f5-6cbbf365adb0
  Args:
    relation: :hasRelation
    source: Ferdinand_dOrleans
    target: Dona_Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AddLiteral (823a141c-d2af-4acf-ae9d-e7baab8ff27a)
 Call ID: 823a141c-d2af-4acf-ae9d-e7baab8ff27a
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1921
    source: Ferdinand_dOrleans
  AssignClass (a8a3bf5e-aa2a-4a46-9e14-d9adc27e7f17)
 Call ID: a8a3bf5e-aa2a-4a46-9e14-d9adc27e7f17
  Args:
    source: Don_Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
    type: :Man
  AssignClass (8ec9d9e5-d558-4e0f-b8cc-56eb3cf2e135)
 Call ID: 8ec9d9e5-d558-4e0f-b8cc-56eb3cf2e135
  Args:
    source: Don_Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
    type: :Person
  AssignClass (f15c80c7-bbd7-444a-9b51-c4c15b428ea8)
 Call ID: f15c80c7-bbd7-444a-9b51-c4c15b428ea8
  Args:
    source: Dona_Isabel_de_Ibarreta_y_Uhagon
    type: :Woman
  AssignClass (23614d41-b443-4942-891b-1e5f60045f95)
 Call ID: 23614d41-b443-4942-891b-1e5f60045f95
  Args:
    source: Dona_Isabel_de_Ibarreta_y_Uhagon
    type: :Person
  AddTriple (81d706ed-93ca-4fce-9f20-31b3884dd0f6)
 Call ID: 81d706ed-93ca-4fce-9f20-31b3884dd0f6
  Args:
    source: Dona_Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
    target: Don_Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
    relation: :hasFather
  AddTriple (13a6843f-c64a-43ff-a1a0-b17bc9913202)
 Call ID: 13a6843f-c64a-43ff-a1a0-b17bc9913202
  Args:
    relation: :hasMother
    source: Dona_Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
    target: Dona_Isabel_de_Ibarreta_y_Uhagon
  Finish (6dda96f0-f9a4-4e53-8bc4-d7abcce96f6b)
 Call ID: 6dda96f0-f9a4-4e53-8bc4-d7abcce96f6b
  Args: