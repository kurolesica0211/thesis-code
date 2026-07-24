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
Margaret of Prussia (German: Margarethe Beatrice Feodora; 22 April 1872 – 22 January 1954) was the youngest child of Frederick III, German Emperor, and Victoria, Princess Royal.
She was also the younger sister of Emperor Wilhelm II and the granddaughter of Queen Victoria.
She married Prince Frederick Charles of Hesse, the elected King of Finland, making her the would-be Queen of Finland had he not decided to renounce the throne on 14 December 1918.
In 1926, they assumed the titles of Landgrave and Landgravine of Hesse.
Early life

Princess Margaret of Prussia was the youngest of eight children born to Frederick III, then Crown Prince of the German Empire, and Victoria, Princess Royal, Britain's Queen Victoria's eldest daughter.
Born on 22 April 1872 in the Hohenzollerns' New Palace in Potsdam, by the time the infant was christened, her head was covered with short hair like moss, from which she acquired her nickname "Mossy".
Crown Princess Margherita of Italy was her godmother and Emperor Pedro II of Brazil was her godfather.
Princess Margaret grew up amid great privilege and formality.
Together with her sisters, Princess Viktoria and Princess Sophie, Margaret was deeply attached to her parents, forming an antagonist group to that of her eldest siblings, William II, Princess Charlotte and Prince Henry.
Margaret was widely regarded as the most popular of Kaiser Wilhelm II's sisters, and she maintained good relations with a wide array of family members.
She was the first cousin of both King George V of the United Kingdom and Empress Alexandra of Russia, all three being grandchildren of Victoria.
As an adult, she was said to resemble her aunt, Princess Alice.
Marriage

Princess Margaret was first attracted to Prince Maximilian of Baden.
When he did not reciprocate her affection, she moved on to her second choice, Max's close friend, Prince Frederick Charles of Hesse, future head of the Hesse-Kassel dynasty and future elected King of Finland.
At the time of the wedding, Prince Frederick Charles was not the Head of the House of Hesse-Kassel.
Prince Frederick Charles, as was his title when he married, was addressed as His Highness, while Princess Margaret warranted Royal Highness.
This disparity came to an end in 1925 when Frederick Charles became Landgrave of Hesse and Head of the house of Hesse-Kassel.
They were second cousins, both great-grandchildren of King Friedrich Wilhelm III of Prussia, he through his mother Anna, she through her father Friedrich.
Initially, her brother Wilhelm opposed the match as he felt that Frederick Charles's position was too "minor" for the Kaiser's sister.
Later, however, he gave his blessing, since Margaret herself "was so unimportant".
Princess Margaret had a strong personality; she always seemed more secure and grounded than her husband.
Margaret's husband was her mother's favorite son-in-law.
In 1901, Princess Margaret inherited Schloss Friedrichshof at the death of her mother.
However, Margaret was committed to maintain the house of her mother which entailed a great expense and the family moved to Friedrichshof.
In 1918, Margaret's husband accepted the offer of the throne of newly independent Finland, but due to German misfortunes in World War I, soon renounced it.
Family tragedies

Margaret's elder sons, Friedrich Wilhelm and Maximilian, were killed in action during World War I. Prince Maximilian, Princess Margaret's second and favorite son, was serving near Aisne when he was seriously wounded by machine gun fire in October 1914.
Princess Margaret's oldest son, Friedrich Wilhelm, died on 12 September 1916 at Kara Orman in Romania.
Her two other sons, Philipp and Christoph, embraced Nazism, and Margaret, who was the sister of the last Kaiser Wilhelm II, invited Adolf Hitler to tea and flew the swastika from her home at Schloss Kronberg.
Philipp married Princess Mafalda, daughter of King Victor Emmanuel III of Italy.
Margaret's fifth son, Christoph, was a staunch supporter of the German war effort, but after the Battle of Stalingrad, he became frustrated by the limitations placed on his own role in the conflict, and increasingly critical of the German leadership.
He was married to Princess Sophie of Greece, sister of Philip, Prince of Greece and Denmark who, in 1947, married the heir to the throne of the United Kingdom and, in 1952, became Prince Philip, Duke of Edinburgh, consort of Queen Elizabeth II.
Margaret also lost another one of her daughters-in-law during the war.
Wolfgang's wife, Princess Marie Alexandra, when she and seven other women war aid workers, were killed in a bomb attack on Frankfurt on 29–30 January 1944.
Margaret, very much the matriarch, was at the centre of her large and dynamic family.
Last years

Landgravine Margaret had difficult years after 1945; they were compounded by the theft from Schloss Friedrichshof in November 1945 of the family jewellery, valued at over £2,000,000.
Princess Margaret's son Wolfgang, fearing for the jewels, had buried them in a sub-cellar of the castle.
In early 1946, Princess Margaret discovered the theft when the family wanted to use the jewels for the wedding of Princess Sophia who was preparing to remarry.
Princess Sophia and Landgravine Margaret reported it to the Frankfurt authorities, and the culprits were imprisoned in August 1951.
The Hesse family received what had been recovered: only 10 percent of what had been stolen.
Landgravine Margaret, the last surviving child of Emperor Frederick III and last grandchild of emperor Emperor Wilhelm I, died in Kronberg on 22 January 1954, 14 years after her husband and exactly 53 years to the day after her British grandmother Queen Victoria.
Children

Landgravine Margaret and her husband Frederick Charles of Hesse had six sons, including two sets of twins:


Archives

Margaret's personal papers (including family correspondence) are preserved in the Archive of the House of Hesse, which is kept in Fasanerie Palace in Eichenzell, Germany.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (812e607a-3fda-4487-aaff-4bbcf0c6a1d4)
 Call ID: 812e607a-3fda-4487-aaff-4bbcf0c6a1d4
  Args:
    source: :Margaret_of_Prussia
    type: :Woman
  AssignClass (d0556db1-8557-4ecc-9fcf-aea0c14eab21)
 Call ID: d0556db1-8557-4ecc-9fcf-aea0c14eab21
  Args:
    source: :Margaret_of_Prussia
    type: :Person
  AssignClass (bac6acaf-802a-4002-b0ed-6e7dbeb12d3d)
 Call ID: bac6acaf-802a-4002-b0ed-6e7dbeb12d3d
  Args:
    source: :Frederick_III
    type: :Man
  AssignClass (ea879111-b6f6-46c4-be70-21a1c9d97a97)
 Call ID: ea879111-b6f6-46c4-be70-21a1c9d97a97
  Args:
    source: :Frederick_III
    type: :Person
  AssignClass (dd6b3fc7-162c-4777-9d7e-1327a38023ff)
 Call ID: dd6b3fc7-162c-4777-9d7e-1327a38023ff
  Args:
    source: :Frederick_III
    type: :Ancestor
  AssignClass (6a9e8cfd-31d5-42b1-bd86-8f24fa6738e2)
 Call ID: 6a9e8cfd-31d5-42b1-bd86-8f24fa6738e2
  Args:
    type: :Woman
    source: :Victoria_Princess_Royal
  AssignClass (fab463f6-c1c6-414e-b10e-050b6e682267)
 Call ID: fab463f6-c1c6-414e-b10e-050b6e682267
  Args:
    type: :Person
    source: :Victoria_Princess_Royal
  AssignClass (d214ec8d-a647-4060-9ea3-b44a23fdb367)
 Call ID: d214ec8d-a647-4060-9ea3-b44a23fdb367
  Args:
    source: :Victoria_Princess_Royal
    type: :Ancestor
  AddLiteral (7a8aadd6-c20a-4be7-9ad8-bcac43d323a4)
 Call ID: 7a8aadd6-c20a-4be7-9ad8-bcac43d323a4
  Args:
    source: :Margaret_of_Prussia
    literal_value: 1872
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (88e06d14-ed72-4feb-b9a8-a3bce8e6a8b5)
 Call ID: 88e06d14-ed72-4feb-b9a8-a3bce8e6a8b5
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1954
    source: :Margaret_of_Prussia
  AddTriple (713ccd9b-e112-4495-93b6-037e6e2db025)
 Call ID: 713ccd9b-e112-4495-93b6-037e6e2db025
  Args:
    source: :Margaret_of_Prussia
    target: :Frederick_III
    relation: :hasFather
  AddTriple (8e065c1a-2806-4666-a0ce-e1379c2a9a8c)
 Call ID: 8e065c1a-2806-4666-a0ce-e1379c2a9a8c
  Args:
    source: :Margaret_of_Prussia
    target: :Victoria_Princess_Royal
    relation: :hasMother
  AssignClass (db143c48-4bcf-4789-8895-26b05cb448bb)
 Call ID: db143c48-4bcf-4789-8895-26b05cb448bb
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (8ead99cd-c07d-4d75-8cf4-4a67d37a345b)
 Call ID: 8ead99cd-c07d-4d75-8cf4-4a67d37a345b
  Args:
    source: :Wilhelm_II
    type: :Person
  AddTriple (3ceff52e-ac4d-4f70-999f-48d276791164)
 Call ID: 3ceff52e-ac4d-4f70-999f-48d276791164
  Args:
    source: :Margaret_of_Prussia
    target: :Wilhelm_II
    relation: :isSiblingOf
  AssignClass (5f13253b-856c-44c2-86ff-21d6b520d752)
 Call ID: 5f13253b-856c-44c2-86ff-21d6b520d752
  Args:
    type: :Woman
    source: :Queen_Victoria
  AssignClass (c3939837-4a5c-4a40-9fb4-c7624fde90fe)
 Call ID: c3939837-4a5c-4a40-9fb4-c7624fde90fe
  Args:
    source: :Queen_Victoria
    type: :Person
  AssignClass (00596c85-b7b3-4949-977a-cf70290122df)
 Call ID: 00596c85-b7b3-4949-977a-cf70290122df
  Args:
    source: :Queen_Victoria
    type: :Ancestor
  AddTriple (e4005c73-fd40-4763-8b0b-e6ba8766c15a)
 Call ID: e4005c73-fd40-4763-8b0b-e6ba8766c15a
  Args:
    relation: :hasAncestor
    target: :Queen_Victoria
    source: :Margaret_of_Prussia
  AssignClass (8ab89872-f5ef-4bfd-8e93-f9049528ecd9)
 Call ID: 8ab89872-f5ef-4bfd-8e93-f9049528ecd9
  Args:
    type: :Man
    source: :Frederick_Charles_of_Hesse
  AssignClass (1e69685e-e661-431d-9516-fb696b4ca0c8)
 Call ID: 1e69685e-e661-431d-9516-fb696b4ca0c8
  Args:
    type: :Person
    source: :Frederick_Charles_of_Hesse
  AssignClass (08f8f0b3-a911-491a-9e09-48e49a2d01b7)
 Call ID: 08f8f0b3-a911-491a-9e09-48e49a2d01b7
  Args:
    type: :Ancestor
    source: :Frederick_Charles_of_Hesse
  AddTriple (d48ab709-c25d-4d15-a348-9e950a132240)
 Call ID: d48ab709-c25d-4d15-a348-9e950a132240
  Args:
    source: :Margaret_of_Prussia
    target: :Frederick_Charles_of_Hesse
    relation: :hasRelation
  AssignClass (2079918a-ed2a-42d7-aef0-c9e374d4f00c)
 Call ID: 2079918a-ed2a-42d7-aef0-c9e374d4f00c
  Args:
    type: :Woman
    source: :Viktoria
  AssignClass (b1e54093-a81b-46c7-9418-04767d6e16ed)
 Call ID: b1e54093-a81b-46c7-9418-04767d6e16ed
  Args:
    type: :Person
    source: :Viktoria
  AssignClass (f66effcc-9162-49f7-a847-49d626e2cb18)
 Call ID: f66effcc-9162-49f7-a847-49d626e2cb18
  Args:
    source: :Sophie
    type: :Woman
  AssignClass (8331df4c-d2a5-42a0-9df1-7a097f299512)
 Call ID: 8331df4c-d2a5-42a0-9df1-7a097f299512
  Args:
    source: :Sophie
    type: :Person
  AssignClass (7f983a9c-64f2-43af-af22-2655e2f31912)
 Call ID: 7f983a9c-64f2-43af-af22-2655e2f31912
  Args:
    source: :Charlotte
    type: :Woman
  AssignClass (a71f9178-2e3a-4096-832c-3f6be88bced9)
 Call ID: a71f9178-2e3a-4096-832c-3f6be88bced9
  Args:
    type: :Person
    source: :Charlotte
  AssignClass (94aec5d1-959f-44fc-911e-c03a112d525b)
 Call ID: 94aec5d1-959f-44fc-911e-c03a112d525b
  Args:
    source: :Henry
    type: :Man
  AssignClass (bb49c3ec-1f20-4b9c-95de-4362cf4358f5)
 Call ID: bb49c3ec-1f20-4b9c-95de-4362cf4358f5
  Args:
    source: :Henry
    type: :Person
  AddTriple (be2ac2fb-6a54-4ec9-b4d2-5d265c835fa9)
 Call ID: be2ac2fb-6a54-4ec9-b4d2-5d265c835fa9
  Args:
    relation: :isSiblingOf
    target: :Viktoria
    source: :Margaret_of_Prussia
  AddTriple (a0da2009-a9e4-4967-b011-ddbdcc10c9e6)
 Call ID: a0da2009-a9e4-4967-b011-ddbdcc10c9e6
  Args:
    source: :Margaret_of_Prussia
    target: :Sophie
    relation: :isSiblingOf
  AddTriple (deed65aa-5cff-42ee-9902-fa3fd92437f7)
 Call ID: deed65aa-5cff-42ee-9902-fa3fd92437f7
  Args:
    source: :Margaret_of_Prussia
    relation: :isSiblingOf
    target: :Charlotte
  AddTriple (0daf22df-44d4-4904-b232-343cd2c3a46a)
 Call ID: 0daf22df-44d4-4904-b232-343cd2c3a46a
  Args:
    target: :Henry
    relation: :isSiblingOf
    source: :Margaret_of_Prussia
  Finish (ae7771a1-633a-45a8-a50d-1dbc1bfccc6f)
 Call ID: ae7771a1-633a-45a8-a50d-1dbc1bfccc6f
  Args: