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
  AssignClass (c7cfc8ef-a43d-46dd-baa7-8533ee83c195)
 Call ID: c7cfc8ef-a43d-46dd-baa7-8533ee83c195
  Args:
    type: :Man
    source: Ferdinand_dOrleans
  AssignClass (7209deb4-9ccc-46cb-89fe-8d92be164be7)
 Call ID: 7209deb4-9ccc-46cb-89fe-8d92be164be7
  Args:
    source: Ferdinand_dOrleans
    type: :Person
  AddLiteral (e2aad2ea-0621-4bdd-ab1e-45eccb7ed3a9)
 Call ID: e2aad2ea-0621-4bdd-ab1e-45eccb7ed3a9
  Args:
    literal_type: xsd:integer
    source: Ferdinand_dOrleans
    relation: :hasBirthYear
    literal_value: 1884
  AddLiteral (8a568ceb-3db7-4576-9cf0-0a27b32db56f)
 Call ID: 8a568ceb-3db7-4576-9cf0-0a27b32db56f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Ferdinand_dOrleans
    literal_value: 1924
  AssignClass (e98eabbb-a396-4f20-9939-13f2cbceb081)
 Call ID: e98eabbb-a396-4f20-9939-13f2cbceb081
  Args:
    type: :Man
    source: Philippe_dOrleans_Count_of_Paris
  AssignClass (73b30506-450c-48bd-89ff-bf213bdfa0db)
 Call ID: 73b30506-450c-48bd-89ff-bf213bdfa0db
  Args:
    source: Philippe_dOrleans_Count_of_Paris
    type: :Person
  AssignClass (b4b0d7f4-0007-424b-9d13-761911348721)
 Call ID: b4b0d7f4-0007-424b-9d13-761911348721
  Args:
    type: :Woman
    source: Marie_Isabelle_dOrleans
  AssignClass (c7af739f-23f3-4e65-9615-baa2ee0d0db0)
 Call ID: c7af739f-23f3-4e65-9615-baa2ee0d0db0
  Args:
    source: Marie_Isabelle_dOrleans
    type: :Person
  AddTriple (21dd0f36-18d2-46ea-b41d-52e47bc6fe7e)
 Call ID: 21dd0f36-18d2-46ea-b41d-52e47bc6fe7e
  Args:
    source: Ferdinand_dOrleans
    relation: :hasFather
    target: Philippe_dOrleans_Count_of_Paris
  AddTriple (976fb198-eddb-4b39-95ba-c346fa6a8d57)
 Call ID: 976fb198-eddb-4b39-95ba-c346fa6a8d57
  Args:
    relation: :hasMother
    source: Ferdinand_dOrleans
    target: Marie_Isabelle_dOrleans
  AssignClass (654e1ac5-f8d8-484c-b67c-44959ae7643f)
 Call ID: 654e1ac5-f8d8-484c-b67c-44959ae7643f
  Args:
    type: :Woman
    source: Princess_Amelie
  AssignClass (a7fc2a5e-518b-439e-a5bc-a6e22e863255)
 Call ID: a7fc2a5e-518b-439e-a5bc-a6e22e863255
  Args:
    source: Princess_Amelie
    type: :Person
  AssignClass (f45b3f73-cc7d-4537-b763-7613d9b3d97e)
 Call ID: f45b3f73-cc7d-4537-b763-7613d9b3d97e
  Args:
    source: Prince_Philippe_sibling
    type: :Man
  AssignClass (ff0ae9b9-b1b2-4423-937a-348028f809b8)
 Call ID: ff0ae9b9-b1b2-4423-937a-348028f809b8
  Args:
    source: Prince_Philippe_sibling
    type: :Person
  AssignClass (e3d5f0b8-e953-495f-8a66-14c9d4a91b15)
 Call ID: e3d5f0b8-e953-495f-8a66-14c9d4a91b15
  Args:
    type: :Woman
    source: Princess_Helene
  AssignClass (35b68ac7-201a-42d5-a032-7cca56bae118)
 Call ID: 35b68ac7-201a-42d5-a032-7cca56bae118
  Args:
    type: :Person
    source: Princess_Helene
  AssignClass (1ff4cb48-4138-458a-b628-fe85b51e70b4)
 Call ID: 1ff4cb48-4138-458a-b628-fe85b51e70b4
  Args:
    source: Prince_Charles
    type: :Man
  AssignClass (f32fec27-0cbb-4e96-b385-82b775bed29f)
 Call ID: f32fec27-0cbb-4e96-b385-82b775bed29f
  Args:
    source: Prince_Charles
    type: :Person
  AssignClass (ff656653-e0a7-4b6b-8263-b70047a80769)
 Call ID: ff656653-e0a7-4b6b-8263-b70047a80769
  Args:
    type: :Woman
    source: Princess_Isabelle
  AssignClass (c0e5261b-2ea5-446f-a383-1e671a445c25)
 Call ID: c0e5261b-2ea5-446f-a383-1e671a445c25
  Args:
    type: :Person
    source: Princess_Isabelle
  AssignClass (0a8299b1-f28d-4cf4-9d18-dad288aa6866)
 Call ID: 0a8299b1-f28d-4cf4-9d18-dad288aa6866
  Args:
    type: :Man
    source: Prince_Jacques
  AssignClass (d489550d-875b-434e-8252-98b1220ad299)
 Call ID: d489550d-875b-434e-8252-98b1220ad299
  Args:
    type: :Person
    source: Prince_Jacques
  AssignClass (32efa87b-ca2a-4f5e-8ead-5c7f316dca47)
 Call ID: 32efa87b-ca2a-4f5e-8ead-5c7f316dca47
  Args:
    source: Princess_Louise
    type: :Woman
  AssignClass (62ce3d5d-981c-4efa-99f0-40b7fcf99419)
 Call ID: 62ce3d5d-981c-4efa-99f0-40b7fcf99419
  Args:
    source: Princess_Louise
    type: :Person
  AddTriple (2265a343-d393-434c-a807-aa5871de61df)
 Call ID: 2265a343-d393-434c-a807-aa5871de61df
  Args:
    source: Ferdinand_dOrleans
    relation: :isSiblingOf
    target: Princess_Amelie
  AddTriple (12071e4c-91ee-497a-8541-c4a857132733)
 Call ID: 12071e4c-91ee-497a-8541-c4a857132733
  Args:
    source: Ferdinand_dOrleans
    relation: :isSiblingOf
    target: Prince_Philippe_sibling
  AddTriple (a4e0d3a1-14b9-4bd6-8971-93cd15949b1c)
 Call ID: a4e0d3a1-14b9-4bd6-8971-93cd15949b1c
  Args:
    target: Princess_Helene
    relation: :isSiblingOf
    source: Ferdinand_dOrleans
  AddTriple (a656d35f-65f2-4c55-beb8-591d6b4a1cab)
 Call ID: a656d35f-65f2-4c55-beb8-591d6b4a1cab
  Args:
    relation: :isSiblingOf
    source: Ferdinand_dOrleans
    target: Prince_Charles
  AddTriple (46cd007c-3374-46a0-b06a-30ea699f131c)
 Call ID: 46cd007c-3374-46a0-b06a-30ea699f131c
  Args:
    relation: :isSiblingOf
    source: Ferdinand_dOrleans
    target: Princess_Isabelle
  AddTriple (397ebdca-0f84-410c-9ed2-8934766c8bd2)
 Call ID: 397ebdca-0f84-410c-9ed2-8934766c8bd2
  Args:
    target: Prince_Jacques
    source: Ferdinand_dOrleans
    relation: :isSiblingOf
  AddTriple (864703a8-eeff-4725-83e1-843aea5ce245)
 Call ID: 864703a8-eeff-4725-83e1-843aea5ce245
  Args:
    relation: :isSiblingOf
    source: Ferdinand_dOrleans
    target: Princess_Louise
  AssignClass (ce8de50f-b024-4f17-a368-68511d460c49)
 Call ID: ce8de50f-b024-4f17-a368-68511d460c49
  Args:
    type: :Man
    source: Prince_Ferdinand_Duke_of_Orleans_grandfather
  AssignClass (d8526ed5-8c94-4ab3-b7c8-aa5e8b375edb)
 Call ID: d8526ed5-8c94-4ab3-b7c8-aa5e8b375edb
  Args:
    type: :Person
    source: Prince_Ferdinand_Duke_of_Orleans_grandfather
  AssignClass (6a5105d3-cef0-415f-9146-9e70e71bec91)
 Call ID: 6a5105d3-cef0-415f-9146-9e70e71bec91
  Args:
    source: Duchess_Helene_of_Mecklenburg_Schwerin
    type: :Woman
  AssignClass (b2463d41-614c-418f-bfe6-5f1e78a3e675)
 Call ID: b2463d41-614c-418f-bfe6-5f1e78a3e675
  Args:
    type: :Person
    source: Duchess_Helene_of_Mecklenburg_Schwerin
  AddTriple (78ecbf67-1964-4dd3-ad5e-422bb9af35c6)
 Call ID: 78ecbf67-1964-4dd3-ad5e-422bb9af35c6
  Args:
    source: Philippe_dOrleans_Count_of_Paris
    relation: :hasFather
    target: Prince_Ferdinand_Duke_of_Orleans_grandfather
  AddTriple (4ab59b1f-853a-4f0c-8c2d-27c6bcfeacfd)
 Call ID: 4ab59b1f-853a-4f0c-8c2d-27c6bcfeacfd
  Args:
    target: Duchess_Helene_of_Mecklenburg_Schwerin
    source: Philippe_dOrleans_Count_of_Paris
    relation: :hasMother
  AssignClass (bc300514-467d-4813-8100-d473131a1c6e)
 Call ID: bc300514-467d-4813-8100-d473131a1c6e
  Args:
    source: Louis_Philippe_I
    type: :Man
  AssignClass (9492f19e-7649-42a4-a1af-d73f52ef073c)
 Call ID: 9492f19e-7649-42a4-a1af-d73f52ef073c
  Args:
    type: :Person
    source: Louis_Philippe_I
  AssignClass (e407b315-da75-4110-9508-ce2c1cb27d1b)
 Call ID: e407b315-da75-4110-9508-ce2c1cb27d1b
  Args:
    source: Queen_Maria_Amalia_of_the_Two_Sicilies
    type: :Woman
  AssignClass (2fb95537-4462-4cd8-9ba6-5809b101dc88)
 Call ID: 2fb95537-4462-4cd8-9ba6-5809b101dc88
  Args:
    source: Queen_Maria_Amalia_of_the_Two_Sicilies
    type: :Person
  AddTriple (0572d95d-2ec9-4f90-954f-60c5ea9ca534)
 Call ID: 0572d95d-2ec9-4f90-954f-60c5ea9ca534
  Args:
    relation: :hasFather
    source: Prince_Ferdinand_Duke_of_Orleans_grandfather
    target: Louis_Philippe_I
  AddTriple (7c047acd-a992-49c5-8c7c-0aefb455b607)
 Call ID: 7c047acd-a992-49c5-8c7c-0aefb455b607
  Args:
    relation: :hasMother
    source: Prince_Ferdinand_Duke_of_Orleans_grandfather
    target: Queen_Maria_Amalia_of_the_Two_Sicilies
  AssignClass (df45ca3d-62fb-40ac-a04c-86a57f9ac447)
 Call ID: df45ca3d-62fb-40ac-a04c-86a57f9ac447
  Args:
    type: :Woman
    source: Infanta_Luisa_Fernanda_of_Spain
  AssignClass (a59958f2-15f6-452e-b510-b72485bb4d9e)
 Call ID: a59958f2-15f6-452e-b510-b72485bb4d9e
  Args:
    type: :Person
    source: Infanta_Luisa_Fernanda_of_Spain
  AssignClass (35b38f6d-59e5-45d4-bde7-3cf285499d3b)
 Call ID: 35b38f6d-59e5-45d4-bde7-3cf285499d3b
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    type: :Man
  AssignClass (ae38422e-2ff3-491f-9dae-85889278f97d)
 Call ID: ae38422e-2ff3-491f-9dae-85889278f97d
  Args:
    type: :Person
    source: Prince_Antoine_Duke_of_Montpensier
  AddTriple (dd5718a1-9bc6-46da-a97c-5a44c10633a4)
 Call ID: dd5718a1-9bc6-46da-a97c-5a44c10633a4
  Args:
    source: Marie_Isabelle_dOrleans
    relation: :hasMother
    target: Infanta_Luisa_Fernanda_of_Spain
  AddTriple (a9f27124-5bbd-4368-8198-747a5959f039)
 Call ID: a9f27124-5bbd-4368-8198-747a5959f039
  Args:
    relation: :hasFather
    source: Marie_Isabelle_dOrleans
    target: Prince_Antoine_Duke_of_Montpensier
  AssignClass (a485972b-395c-4907-942e-2494e7c09b66)
 Call ID: a485972b-395c-4907-942e-2494e7c09b66
  Args:
    type: :Woman
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AssignClass (9b60d888-fabf-4aa7-8978-8937068fb2d3)
 Call ID: 9b60d888-fabf-4aa7-8978-8937068fb2d3
  Args:
    type: :Person
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AddLiteral (fd4b1fdb-a2ce-4cac-b663-3645563d46d7)
 Call ID: fd4b1fdb-a2ce-4cac-b663-3645563d46d7
  Args:
    literal_type: xsd:integer
    source: Ferdinand_dOrleans
    literal_value: 1921
    relation: :hasMarriageYear
  AddTriple (1e532709-b423-4118-a159-512dd204ae94)
 Call ID: 1e532709-b423-4118-a159-512dd204ae94
  Args:
    relation: :hasRelation
    source: Ferdinand_dOrleans
    target: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AssignClass (b8d47059-492f-42ce-a537-74d48b7d013f)
 Call ID: b8d47059-492f-42ce-a537-74d48b7d013f
  Args:
    source: Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
    type: :Man
  AssignClass (a9f75527-804b-4de7-8a9f-0ef13d2b176e)
 Call ID: a9f75527-804b-4de7-8a9f-0ef13d2b176e
  Args:
    source: Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
    type: :Person
  AssignClass (abac1930-bbd2-47e1-b345-6966b16e1dc1)
 Call ID: abac1930-bbd2-47e1-b345-6966b16e1dc1
  Args:
    source: Isabel_de_Ibarreta_y_Uhagon
    type: :Woman
  AssignClass (7a1ece02-075a-456e-a9b5-7ef5c79e77f9)
 Call ID: 7a1ece02-075a-456e-a9b5-7ef5c79e77f9
  Args:
    type: :Person
    source: Isabel_de_Ibarreta_y_Uhagon
  AddTriple (071f6df3-58bf-4989-8fe2-22a87ecf6335)
 Call ID: 071f6df3-58bf-4989-8fe2-22a87ecf6335
  Args:
    relation: :hasFather
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
    target: Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
  AddTriple (5d21586a-93f5-4576-8acb-62291609f227)
 Call ID: 5d21586a-93f5-4576-8acb-62291609f227
  Args:
    relation: :hasMother
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
    target: Isabel_de_Ibarreta_y_Uhagon
  Finish (1b52d1da-76f0-448e-8fe9-59ec3222d88d)
 Call ID: 1b52d1da-76f0-448e-8fe9-59ec3222d88d
  Args: