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
Prince Philippe, Duke of Orléans (French: Louis Philippe Robert; 6 February 1869 – 28 March 1926) was the Orléanist pretender to the throne of France from 1894 to 1926 as Philippe VIII.
Early life

Philippe was born at York House, Twickenham, near London, the son of Philippe, Count of Paris, by his wife (and first cousin), Princess Isabelle of Orléans.
He was baptised with the names Louis-Philippe-Robert, and was called Philippe.
His family lived in the United Kingdom from the abdication and banishment of his great-grandfather Louis Philippe I, King of the French, in 1848, and returned to France in 1871 following the fall of the Second French Empire.
However, they again took refuge in England in 1886, when the French Republic exiled them following the wedding in Paris of Philippe's sister Amélie of Orléans to Crown Prince Carlos of Portugal.
Returning therefore to France in 1871 with his parents, Philippe was educated at home at the Château d'Eu and at the Collège Stanislas de Paris.
In 1880 Philippe's father granted him the title Duc d'Orléans.
Military career

Philippe began his military education at the École spéciale militaire de Saint-Cyr.
In October 1889, Philippe went to Switzerland to complete a course in military theory.
While there he fathered a son, Philippe Debien, by Nina, an actress working in the casino at Lausanne.
Drawn to explore the "unknown", Philippe asked Prince George, Duke of Cambridge, to send him to a military post in the Himalayas.
While in the East, he undertook a hunting and exploratory expedition in Nepal with his cousin Prince Henri of Orléans, went mountain-climbing in Tibet, and visited Afghanistan, Ceylon, and the Persian Gulf, before being posted back to Britain.
Prior to his imprisonment in France, Philippe had been unofficially engaged to his first cousin Princess Marguerite of Orléans, but the engagement was cancelled when Philippe's involvement with the Australian opera singer Nellie Melba was revealed.
Armstrong filed for divorce from Melba on the grounds of adultery, naming Philippe as co-respondent; the case was eventually dropped.
In September 1890, Philippe accompanied his father on a two-month trip to the United States and Canada.
On 12 November 1890, while in Philadelphia, Philippe joined the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States (MOLLUS) - a military society composed of officers who had served the Union in the American Civil War and their descendants - by right of his father's service in the Union Army.
In December 1890, Philippe applied unsuccessfully to serve in the Russian Army.
In March 1894, Philippe went to Egypt and Palestine with his sister Hélène, Duchess of Aosta.
Claimant to the defunct throne

Upon the death of his father on 8 September 1894, Philippe became the Orléanist claimant to the defunct French throne.
He was known to monarchists as Philippe VIII.
In October 1895, Philippe was named as co-respondent in the divorce case of Woolston v. Woolston.
Unlike his great grandfather, Louis Philippe I, Philippe claimed grand mastership of the Order of the Holy Spirit as intrinsic to his dynastic claim to the throne, and sometimes wore the breast star of the order.
On 5 November 1896, in Vienna, Philippe married Archduchess Maria Dorothea of Austria (1867–1932), a daughter of Archduke Joseph Karl of Austria, Palatine of Hungary, and granddaughter of Princess Clémentine of Orléans, as well as a niece of Marie Henriette of Austria, Queen Consort of the Belgians.
While travelling in Geneva in 1898, Philippe narrowly missed being assassinated by Luigi Lucheni, an anarchist, who vowed to kill the next member of a royal family that he saw.
He explored parts of the northeastern coast of Greenland, Denmark, in 1905 during his Duke of Orléans Arctic Expedition on ship Belgica.
Philippe continued to reside in the United Kingdom until 1912, when he moved his primary residence to Belgium.
In 1914, Philippe and his wife Maria Dorothea were legally separated.
At the outbreak of the First World War, Philippe again tried unsuccessfully to join the French army.
In 1926, Philippe died of pneumonia at the Palais d'Orléans in Palermo, Sicily, Italy.
Having no legitimate issue, he was succeeded as pretender to the defunct throne of France by his cousin and brother in law, Jean, Duke of Guise.
Publications

Philippe wrote a number of works based on his many travels: 


He also published a collection of the papers of his father and of the Henri, comte de Chambord:
Honours

In popular culture

Duke Philippe of Orleans briefly appears in an urban fantasy novel for children, The Master Key (1901) by L. Frank Baum.



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
  AssignClass (7abf8d9e-fd0b-4e58-89bc-dcf91ded151d)
 Call ID: 7abf8d9e-fd0b-4e58-89bc-dcf91ded151d
  Args:
    type: :Man
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (6e564aec-7caa-4e08-8cb8-e85434741aad)
 Call ID: 6e564aec-7caa-4e08-8cb8-e85434741aad
  Args:
    type: :Person
    source: Prince_Philippe_Duke_of_Orleans
  AddLiteral (382bee2f-c006-468b-a34b-d9d55cf052eb)
 Call ID: 382bee2f-c006-468b-a34b-d9d55cf052eb
  Args:
    literal_type: xsd:integer
    literal_value: 1869
    relation: :hasBirthYear
    source: Prince_Philippe_Duke_of_Orleans
  AddLiteral (19ffd060-6a4d-4639-be0d-16e8a8ecc5f0)
 Call ID: 19ffd060-6a4d-4639-be0d-16e8a8ecc5f0
  Args:
    source: Prince_Philippe_Duke_of_Orleans
    literal_type: xsd:integer
    literal_value: 1926
    relation: :hasDeathYear
  AddLiteral (e5589645-b744-49e0-a694-6c5b86a95e67)
 Call ID: e5589645-b744-49e0-a694-6c5b86a95e67
  Args:
    relation: :knownAs
    literal_value: Philippe VIII
    literal_type: xsd:string
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (21afc920-5ce3-4363-9a23-1a9cae69f626)
 Call ID: 21afc920-5ce3-4363-9a23-1a9cae69f626
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (f6856392-0fc9-48ae-8ac3-bf10050e6f69)
 Call ID: f6856392-0fc9-48ae-8ac3-bf10050e6f69
  Args:
    source: Philippe_Count_of_Paris
    type: :Person
  AddTriple (1a701c46-010b-49ce-bdaf-68d584d2e3cb)
 Call ID: 1a701c46-010b-49ce-bdaf-68d584d2e3cb
  Args:
    relation: :hasFather
    target: Philippe_Count_of_Paris
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (7203fbff-997f-493d-bf62-dd4241bf834f)
 Call ID: 7203fbff-997f-493d-bf62-dd4241bf834f
  Args:
    source: Princess_Isabelle_of_Orleans
    type: :Woman
  AssignClass (08d53380-76e5-4b91-8c65-42bf7d6ee07f)
 Call ID: 08d53380-76e5-4b91-8c65-42bf7d6ee07f
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orleans
  AddTriple (a98f33ae-9dd3-4c23-93a0-2d31d7c3c99f)
 Call ID: a98f33ae-9dd3-4c23-93a0-2d31d7c3c99f
  Args:
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (3b0ef8da-0c95-4a93-aaa0-626116aabd41)
 Call ID: 3b0ef8da-0c95-4a93-aaa0-626116aabd41
  Args:
    type: :Man
    source: Philippe_Debien
  AssignClass (19775bb4-83fc-4b6f-8a54-6565863df003)
 Call ID: 19775bb4-83fc-4b6f-8a54-6565863df003
  Args:
    source: Philippe_Debien
    type: :Person
  AddTriple (665c488a-b22c-443b-80ef-e2ef566d9bb1)
 Call ID: 665c488a-b22c-443b-80ef-e2ef566d9bb1
  Args:
    source: Prince_Philippe_Duke_of_Orleans
    target: Philippe_Debien
    relation: :isFatherOf
  AssignClass (b950333f-ef61-43be-b350-ffb32cf0607a)
 Call ID: b950333f-ef61-43be-b350-ffb32cf0607a
  Args:
    source: Nina
    type: :Woman
  AssignClass (3bd856a2-27de-4f80-8c89-af8c03e34bc5)
 Call ID: 3bd856a2-27de-4f80-8c89-af8c03e34bc5
  Args:
    source: Nina
    type: :Person
  AddTriple (f8aef13d-3e0d-41aa-9bb3-f19ebb6cac2c)
 Call ID: f8aef13d-3e0d-41aa-9bb3-f19ebb6cac2c
  Args:
    target: Philippe_Debien
    source: Nina
    relation: :isMotherOf
  AssignClass (be702e06-cc03-4c06-8b16-f986fb5eb02e)
 Call ID: be702e06-cc03-4c06-8b16-f986fb5eb02e
  Args:
    type: :Woman
    source: Amelie_of_Orleans
  AssignClass (e4d61f36-9a51-4000-b4d1-76fbf7526c64)
 Call ID: e4d61f36-9a51-4000-b4d1-76fbf7526c64
  Args:
    source: Amelie_of_Orleans
    type: :Person
  AddTriple (452b3044-a68a-4aed-9d36-9601f298a72f)
 Call ID: 452b3044-a68a-4aed-9d36-9601f298a72f
  Args:
    relation: :isSisterOf
    source: Amelie_of_Orleans
    target: Prince_Philippe_Duke_of_Orleans
  AssignClass (e501ce03-2704-4b8a-87bb-c47c23d263e2)
 Call ID: e501ce03-2704-4b8a-87bb-c47c23d263e2
  Args:
    type: :Woman
    source: Helene_Duchess_of_Aosta
  AssignClass (ea5850fd-7af8-4536-b51e-c004e0198775)
 Call ID: ea5850fd-7af8-4536-b51e-c004e0198775
  Args:
    type: :Person
    source: Helene_Duchess_of_Aosta
  AddTriple (928f5349-e4af-4913-8202-67f5470d4459)
 Call ID: 928f5349-e4af-4913-8202-67f5470d4459
  Args:
    relation: :isSisterOf
    source: Helene_Duchess_of_Aosta
    target: Prince_Philippe_Duke_of_Orleans
  AssignClass (49906cff-b926-4656-b048-cee662bd824c)
 Call ID: 49906cff-b926-4656-b048-cee662bd824c
  Args:
    source: Archduchess_Maria_Dorothea_of_Austria
    type: :Woman
  AssignClass (c559f255-f9ec-4d2d-8bd6-4d073cad9d86)
 Call ID: c559f255-f9ec-4d2d-8bd6-4d073cad9d86
  Args:
    type: :Person
    source: Archduchess_Maria_Dorothea_of_Austria
  AddLiteral (40ffc600-6c0c-4692-8d27-95338c4383cd)
 Call ID: 40ffc600-6c0c-4692-8d27-95338c4383cd
  Args:
    literal_type: xsd:integer
    literal_value: 1896
    relation: :hasMarriageYear
    source: Prince_Philippe_Duke_of_Orleans
  AddTriple (7b6d1361-2e03-4ce4-a85a-20c6ef2fda22)
 Call ID: 7b6d1361-2e03-4ce4-a85a-20c6ef2fda22
  Args:
    relation: :hasRelation
    target: Archduchess_Maria_Dorothea_of_Austria
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (9b5540d0-1a11-4d31-b0b6-dc70319c5255)
 Call ID: 9b5540d0-1a11-4d31-b0b6-dc70319c5255
  Args:
    type: :Man
    source: Archduke_Joseph_Karl_of_Austria
  AssignClass (6875007b-d473-40ec-9d9e-41041ddf9764)
 Call ID: 6875007b-d473-40ec-9d9e-41041ddf9764
  Args:
    source: Archduke_Joseph_Karl_of_Austria
    type: :Person
  AddTriple (ec65b3ad-1ef4-4dee-9b6d-12d2ce146fe0)
 Call ID: ec65b3ad-1ef4-4dee-9b6d-12d2ce146fe0
  Args:
    source: Archduchess_Maria_Dorothea_of_Austria
    target: Archduke_Joseph_Karl_of_Austria
    relation: :hasFather
  AssignClass (8cd15499-3d86-4b5d-afcf-336e31da3611)
 Call ID: 8cd15499-3d86-4b5d-afcf-336e31da3611
  Args:
    source: Jean_Duke_of_Guise
    type: :Man
  AssignClass (cfcd0821-f161-42c9-ae28-ea5198d46453)
 Call ID: cfcd0821-f161-42c9-ae28-ea5198d46453
  Args:
    source: Jean_Duke_of_Guise
    type: :Person
  Finish (0415eca2-8459-458f-8a9c-f773786e1c46)
 Call ID: 0415eca2-8459-458f-8a9c-f773786e1c46
  Args: