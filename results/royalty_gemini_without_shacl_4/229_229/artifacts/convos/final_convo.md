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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (84e2e0b5-a25d-4702-b99b-3405eca4623b)
 Call ID: 84e2e0b5-a25d-4702-b99b-3405eca4623b
  Args:
    type: :Man
    source: :Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (367d77a2-18cf-4938-a9a9-485ce6b9af0c)
 Call ID: 367d77a2-18cf-4938-a9a9-485ce6b9af0c
  Args:
    relation: :hasBirthYear
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    literal_value: 1933
    literal_type: xsd:integer
  AddLiteral (07a0245d-cd32-4a6e-a16a-1fce013aa98e)
 Call ID: 07a0245d-cd32-4a6e-a16a-1fce013aa98e
  Args:
    literal_type: xsd:integer
    literal_value: 2019
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasDeathYear
  AssignClass (04373ed2-073c-41de-8326-14ace40b1419)
 Call ID: 04373ed2-073c-41de-8326-14ace40b1419
  Args:
    type: :Man
    source: :Henri_Count_of_Paris
  AddLiteral (16f108db-6eeb-43c8-9fa0-4d56ea8a2300)
 Call ID: 16f108db-6eeb-43c8-9fa0-4d56ea8a2300
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Henri_Count_of_Paris
    literal_value: 1908
  AddLiteral (25e6b287-3adb-429f-804f-d156f53afeae)
 Call ID: 25e6b287-3adb-429f-804f-d156f53afeae
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1999
    source: :Henri_Count_of_Paris
  AssignClass (ae26c406-0d2e-4e04-bf48-8ca7b3586f1d)
 Call ID: ae26c406-0d2e-4e04-bf48-8ca7b3586f1d
  Args:
    source: :Princess_Isabelle_of_Orleans_Braganza
    type: :Woman
  AddTriple (7765d427-48f1-46a7-ac59-7b36bac7e479)
 Call ID: 7765d427-48f1-46a7-ac59-7b36bac7e479
  Args:
    target: :Henri_Count_of_Paris
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
  AddTriple (e748b58f-7c22-4dd0-a3ef-ac889a21a229)
 Call ID: e748b58f-7c22-4dd0-a3ef-ac889a21a229
  Args:
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    target: :Princess_Isabelle_of_Orleans_Braganza
    relation: :hasMother
  AssignClass (cb5bd908-fdf0-4930-af82-1b7cca0c38aa)
 Call ID: cb5bd908-fdf0-4930-af82-1b7cca0c38aa
  Args:
    type: :Man
    source: :Francois_dOrleans
  AddTriple (c254262b-bb0b-4141-9738-ebf42dc55923)
 Call ID: c254262b-bb0b-4141-9738-ebf42dc55923
  Args:
    relation: :hasBrother
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    target: :Francois_dOrleans
  AssignClass (0e39afdd-a248-42fa-a01a-031c53bd036e)
 Call ID: 0e39afdd-a248-42fa-a01a-031c53bd036e
  Args:
    source: :Duchess_Marie_Therese_of_Wurttemberg
    type: :Woman
  AddLiteral (15967fa3-4bfd-4034-b78e-0a19e4513b1f)
 Call ID: 15967fa3-4bfd-4034-b78e-0a19e4513b1f
  Args:
    literal_type: xsd:integer
    literal_value: 1934
    source: :Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasBirthYear
  AddTriple (347b0839-54a8-4fad-a519-6356a162399d)
 Call ID: 347b0839-54a8-4fad-a519-6356a162399d
  Args:
    target: :Duchess_Marie_Therese_of_Wurttemberg
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasRelation
  AddLiteral (ce847c8d-f03d-4668-a1f4-9f0e06e55bd9)
 Call ID: ce847c8d-f03d-4668-a1f4-9f0e06e55bd9
  Args:
    relation: :hasMarriageYear
    literal_value: 1984
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    literal_type: xsd:integer
  AssignClass (ac8eba26-76ad-4031-bb9e-562ba319f17e)
 Call ID: ac8eba26-76ad-4031-bb9e-562ba319f17e
  Args:
    type: :Woman
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (23d01c7f-3623-4b29-8b6b-edfeedf7e883)
 Call ID: 23d01c7f-3623-4b29-8b6b-edfeedf7e883
  Args:
    literal_type: xsd:integer
    literal_value: 1938
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasBirthYear
  AddLiteral (cdfd8c1d-1894-477b-b819-f63358ca542f)
 Call ID: cdfd8c1d-1894-477b-b819-f63358ca542f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_value: 2022
  AddTriple (cd8042e5-9f8d-4032-bbf5-9d10894270b8)
 Call ID: cd8042e5-9f8d-4032-bbf5-9d10894270b8
  Args:
    relation: :hasRelation
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    target: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (0ef4be2d-317f-4252-b3cb-4e9ada3d2313)
 Call ID: 0ef4be2d-317f-4252-b3cb-4e9ada3d2313
  Args:
    relation: :hasMarriageYear
    literal_value: 1984
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_type: xsd:integer
  AssignClass (4c7dc163-c793-41a0-b68a-f67e1e8addcf)
 Call ID: 4c7dc163-c793-41a0-b68a-f67e1e8addcf
  Args:
    type: :Man
    source: :Luis_Cousino_y_Sebire
  AssignClass (cb663392-6608-429a-8b0e-452abee87645)
 Call ID: cb663392-6608-429a-8b0e-452abee87645
  Args:
    type: :Woman
    source: :Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AddTriple (498b5557-11ca-4e84-b5fd-6afa299ae1ca)
 Call ID: 498b5557-11ca-4e84-b5fd-6afa299ae1ca
  Args:
    relation: :hasFather
    target: :Luis_Cousino_y_Sebire
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddTriple (1928ef55-02f7-4b33-9e81-a3db7ac8cba2)
 Call ID: 1928ef55-02f7-4b33-9e81-a3db7ac8cba2
  Args:
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: :Antonia_Maria_Quinones_de_Leon_y_Banuelos
    relation: :hasMother
  AssignClass (67614db7-c263-4b33-a6ab-b16f69d0c30e)
 Call ID: 67614db7-c263-4b33-a6ab-b16f69d0c30e
  Args:
    source: :Marie_dOrleans
    type: :Woman
  AddTriple (ae8be9da-4e80-408e-af36-8366dc40588d)
 Call ID: ae8be9da-4e80-408e-af36-8366dc40588d
  Args:
    target: :Henri_Philippe_Pierre_Marie_dOrleans
    source: :Marie_dOrleans
    relation: :hasFather
  AddTriple (5a762cee-050d-4458-bf9c-7d2de72a738a)
 Call ID: 5a762cee-050d-4458-bf9c-7d2de72a738a
  Args:
    relation: :hasMother
    target: :Duchess_Marie_Therese_of_Wurttemberg
    source: :Marie_dOrleans
  AssignClass (ee34c062-86f0-4a30-a216-c551a92e03fe)
 Call ID: ee34c062-86f0-4a30-a216-c551a92e03fe
  Args:
    source: :Prince_Gundakar_of_Liechtenstein
    type: :Man
  AddTriple (2798b63c-3c20-4a90-876b-cbf4822584fc)
 Call ID: 2798b63c-3c20-4a90-876b-cbf4822584fc
  Args:
    source: :Marie_dOrleans
    target: :Prince_Gundakar_of_Liechtenstein
    relation: :hasRelation
  AssignClass (62f7f058-90bc-4e75-9ca2-e7422fae0bf0)
 Call ID: 62f7f058-90bc-4e75-9ca2-e7422fae0bf0
  Args:
    type: :Woman
    source: :Diane_dOrleans
  AddTriple (6e22718b-324f-4ca5-8b05-4e9a2bb8a753)
 Call ID: 6e22718b-324f-4ca5-8b05-4e9a2bb8a753
  Args:
    relation: :hasSister
    target: :Diane_dOrleans
    source: :Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (dc9fd196-14d6-4545-b6db-06274ee9ab93)
 Call ID: dc9fd196-14d6-4545-b6db-06274ee9ab93
  Args:
    source: :Michel_dOrleans
    type: :Man
  AddTriple (0a7143c2-cceb-4387-8ff9-9f73ca2352ba)
 Call ID: 0a7143c2-cceb-4387-8ff9-9f73ca2352ba
  Args:
    target: :Michel_dOrleans
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasBrother
  AssignClass (fb9922df-69d4-408c-9fae-df90a81b54a0)
 Call ID: fb9922df-69d4-408c-9fae-df90a81b54a0
  Args:
    type: :Man
    source: :Thibaut_dOrleans
  AddTriple (4fd13803-6cd8-47ae-bd12-a4f0c751430c)
 Call ID: 4fd13803-6cd8-47ae-bd12-a4f0c751430c
  Args:
    relation: :hasBrother
    target: :Thibaut_dOrleans
    source: :Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (952f615c-96c9-4de9-81ff-a3fb660cade2)
 Call ID: 952f615c-96c9-4de9-81ff-a3fb660cade2
  Args:
    source: :Jacques_dOrleans
    type: :Man
  AddTriple (4a6d1f02-e7b6-4e9d-9ab1-9b740d1c17cf)
 Call ID: 4a6d1f02-e7b6-4e9d-9ab1-9b740d1c17cf
  Args:
    source: :Henri_Philippe_Pierre_Marie_dOrleans
    target: :Jacques_dOrleans
    relation: :hasBrother
  AssignClass (302b9e79-31ad-4dae-a1e1-5911f95d8554)
 Call ID: 302b9e79-31ad-4dae-a1e1-5911f95d8554
  Args:
    type: :Man
    source: :Charles_Louis_dOrleans
  AddLiteral (40412a41-8ae6-4206-a53a-42cb5b1bd456)
 Call ID: 40412a41-8ae6-4206-a53a-42cb5b1bd456
  Args:
    literal_type: xsd:integer
    literal_value: 1972
    source: :Charles_Louis_dOrleans
    relation: :hasBirthYear
  AddTriple (135ee84a-8db9-44f7-8802-948b9492fbf8)
 Call ID: 135ee84a-8db9-44f7-8802-948b9492fbf8
  Args:
    target: :Jacques_dOrleans
    source: :Charles_Louis_dOrleans
    relation: :hasFather
  AssignClass (376fb4ce-e608-4409-a3f9-6c2791837da9)
 Call ID: 376fb4ce-e608-4409-a3f9-6c2791837da9
  Args:
    type: :Man
    source: :Foulques_dOrleans
  AddLiteral (580fddd4-6fd0-489c-b8e2-e233da750d03)
 Call ID: 580fddd4-6fd0-489c-b8e2-e233da750d03
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Foulques_dOrleans
    literal_value: 1974
  AddTriple (62e975ff-257f-4bbe-8a76-6278f2beeb33)
 Call ID: 62e975ff-257f-4bbe-8a76-6278f2beeb33
  Args:
    relation: :hasFather
    target: :Jacques_dOrleans
    source: :Foulques_dOrleans
  AssignClass (4c3d78c3-2d65-413c-b045-254c0592592b)
 Call ID: 4c3d78c3-2d65-413c-b045-254c0592592b
  Args:
    source: :Francois_Count_of_Clermont
    type: :Man
  AddTriple (ec74e4e0-0883-437c-be92-ae0f8714d8cc)
 Call ID: ec74e4e0-0883-437c-be92-ae0f8714d8cc
  Args:
    relation: :hasFather
    target: :Henri_Philippe_Pierre_Marie_dOrleans
    source: :Francois_Count_of_Clermont
  AddTriple (232953b7-349a-4d41-b7c9-2ac953f454b8)
 Call ID: 232953b7-349a-4d41-b7c9-2ac953f454b8
  Args:
    relation: :hasMother
    source: :Francois_Count_of_Clermont
    target: :Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (0b346055-fcf4-4181-9040-c8fca75f1c7c)
 Call ID: 0b346055-fcf4-4181-9040-c8fca75f1c7c
  Args:
    source: :Jean_Duke_of_Vendome
    type: :Man
  AddTriple (42734d3a-0dba-48c8-8206-467776fce6ad)
 Call ID: 42734d3a-0dba-48c8-8206-467776fce6ad
  Args:
    target: :Henri_Philippe_Pierre_Marie_dOrleans
    source: :Jean_Duke_of_Vendome
    relation: :hasFather
  AddTriple (f3eed9d9-bfba-43c1-8044-69d2255dfbc8)
 Call ID: f3eed9d9-bfba-43c1-8044-69d2255dfbc8
  Args:
    relation: :hasMother
    source: :Jean_Duke_of_Vendome
    target: :Duchess_Marie_Therese_of_Wurttemberg
  Finish (bf5c31f1-9bb9-424d-b815-175140fb5d6f)
 Call ID: bf5c31f1-9bb9-424d-b815-175140fb5d6f
  Args: